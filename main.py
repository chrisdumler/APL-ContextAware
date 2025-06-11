"""
Enhanced main UI for APL Context-Aware.

Extended from original APL to include context awareness display
and sophisticated agent interaction capabilities.
"""

import os
import uuid
import asyncio
from datetime import datetime
from typing import Any, Dict, List, Optional

from nicegui import ui, app
import langsmith
from langchain_openai import ChatOpenAI

from agent import AgentFactory, AgentConfig
from context_manager import ContextManager
from utils import (
    load_config, 
    save_conversation, 
    load_conversation,
    list_agent_configs,
    save_evaluation,
    logger
)

# Load configuration
config = load_config()

# Initialize the agent factory and context manager
agent_factory = AgentFactory()
context_manager = ContextManager()

# Initialize global variables
current_agent = None
current_agent_config = None
current_conversation_id = str(uuid.uuid4())
messages = []
chat_container = None
context_display_container = None  # NEW: For context information

# Check if default configs exist, if not create them
if not list_agent_configs():
    agent_factory.create_default_configs()

def format_message(message: Dict[str, Any]) -> ui.element:
    """
    Format a message for display in the chat interface.
    
    Args:
        message: Message dictionary
        
    Returns:
        ui.element: Formatted message element
    """
    is_user = message.get("role") == "user"
    
    with ui.card().classes('message-card w-full'):
        with ui.row().classes('w-full items-center mb-2'):
            ui.icon('person' if is_user else 'smart_toy').classes('text-2xl mr-3')
            ui.label(message.get("role", "unknown").capitalize()).classes('font-bold text-gray-700')
            ui.label(message.get("timestamp", "")).classes('text-xs text-gray-500 ml-auto')
        
        with ui.row().classes('w-full'):
            ui.label(message.get("content", "")).classes('whitespace-pre-wrap text-gray-800 leading-relaxed')
        
        # Enhanced context information display
        if message.get("context_info"):
            with ui.row().classes('w-full mt-3 p-2 bg-blue-50 rounded-lg border-l-4 border-blue-400'):
                ui.label("Context:").classes('font-semibold text-blue-700 mr-2')
                energy = message['context_info'].get('energy', 'unknown')
                energy_color = {
                    'high': 'text-red-600 bg-red-100',
                    'medium': 'text-yellow-600 bg-yellow-100', 
                    'low': 'text-blue-600 bg-blue-100'
                }.get(energy, 'text-gray-600 bg-gray-100')
                ui.label(f"{energy.title()} Energy").classes(f'px-2 py-1 rounded text-sm font-medium {energy_color}')
        
        if not is_user and "evaluation" in message:
            with ui.row().classes('w-full mt-2 p-2 bg-gray-50 rounded'):
                ui.label("Evaluation:").classes('font-bold text-gray-700')
                ui.label(message["evaluation"].get("rating", "Not rated")).classes('ml-2 text-gray-600')
                ui.label(message["evaluation"].get("feedback", "")).classes('ml-2 text-gray-600')

def add_message(role: str, content: str, context_info: Dict = None) -> None:
    """
    Add a message to the conversation.
    
    Args:
        role: Role of the message sender (user or assistant)
        content: Content of the message
        context_info: Optional context information (NEW)
    """
    global messages
    
    message = {
        "role": role,
        "content": content,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    # NEW: Add context information if provided
    if context_info:
        message["context_info"] = context_info
    
    messages.append(message)
    save_conversation(current_conversation_id, messages)
    
    if chat_container is not None:
        with chat_container:
            format_message(message)

def update_context_display(context_info: Dict) -> None:
    """
    Update the context display panel.
    
    Args:
        context_info: Context information to display
    """
    if context_display_container is not None:
        context_display_container.clear()
        
        with context_display_container:
            ui.label("Context Awareness").classes('text-lg font-bold mb-2')
            
            if context_info.get("enabled"):
                energy = context_info.get('energy', 'Unknown')
                confidence = context_info.get('confidence', 0)
                reasoning = context_info.get('reasoning', 'No reasoning available')
                
                # Energy level with color coding
                energy_color = {
                    'high': 'text-red-600',
                    'medium': 'text-yellow-600', 
                    'low': 'text-blue-600'
                }.get(energy, 'text-gray-600')
                
                ui.label(f"🔍 Energy Level: {energy.title()}").classes(f'mb-1 {energy_color} font-semibold')
                ui.label(f"📊 Confidence: {confidence:.1%}").classes('mb-1')
                ui.label(f"🎯 Adaptation: {context_info.get('adaptation', 'None')}").classes('mb-1')
                ui.label(f"💭 Reasoning: {reasoning}").classes('mb-1 text-sm text-gray-600')
            else:
                ui.label("Context awareness disabled").classes('text-gray-500')

async def handle_user_message(content: str) -> None:
    """
    Handle a user message.
    
    Args:
        content: Content of the message
    """
    global current_agent, current_agent_config
    
    if not content.strip():
        return
    
    # Clear the input field
    message_input.value = ""
    
    # NEW: Detect context if enabled
    context_info = None
    if current_agent_config and current_agent_config.context_awareness.get("enabled"):
        # Use ContextManager for real energy detection
        detection_result = context_manager.detect_energy_level(content)
        
        context_info = {
            "enabled": True,
            "energy": detection_result["energy"],
            "confidence": detection_result["confidence"],
            "reasoning": detection_result["reasoning"],
            "adaptation": f"Adjusted for {detection_result['energy']} energy"
        }
        
        # Update context display
        update_context_display(context_info)
        
        # Log the detection for debugging
        logger.info(f"Energy detected: {detection_result['energy']} "
                   f"(confidence: {detection_result['confidence']:.2f}) "
                   f"for input: '{content[:50]}...'")
    
    # Add the user message to the conversation
    add_message("user", content, context_info)
    
    # Create or recreate the agent with energy context
    config_name = agent_config_select.value
    
    # Load agent config if not already loaded
    if current_agent_config is None:
        _, current_agent_config = agent_factory.create_agent(config_name)
    
    # If context awareness is enabled and we have energy detection, create agent with energy context
    if (current_agent_config.context_awareness.get("enabled") and 
        current_agent_config.context_awareness.get("behavioral_adaptation") and
        context_info and context_info.get("energy")):
        
        detected_energy = context_info["energy"]
        current_agent, current_agent_config = agent_factory.create_agent(config_name, detected_energy)
        logger.info(f"Created energy-adapted agent for {detected_energy} energy level")
        
    elif current_agent is None:
        # Create agent normally if no context or first time
        current_agent, current_agent_config = agent_factory.create_agent(config_name)
    
    # Show typing indicator
    if chat_container is not None:
        with chat_container:
            typing_indicator = ui.label("Agent is typing...").classes('text-gray-500 italic')
    else:
        typing_indicator = None
    
    try:
        # Get the agent response
        response = await current_agent.ainvoke({"input": content})
        agent_response = response["output"]
        
        # Remove the typing indicator
        if typing_indicator is not None:
            typing_indicator.delete()
        
        # Add the agent response to the conversation
        add_message("assistant", agent_response)
    except Exception as e:
        # Remove the typing indicator
        if typing_indicator is not None:
            typing_indicator.delete()
        
        # Add an error message
        error_message = f"Error: {str(e)}"
        add_message("system", error_message)
        logger.error(f"Error in agent response: {str(e)}")

def handle_agent_config_change(config_name: str) -> None:
    """
    Handle a change in the agent configuration.
    
    Args:
        config_name: Name of the new configuration
    """
    global current_agent, current_agent_config, current_conversation_id, messages
    
    # Create a new agent with the selected configuration
    current_agent, current_agent_config = agent_factory.create_agent(config_name)
    
    # Start a new conversation
    current_conversation_id = str(uuid.uuid4())
    messages = []
    
    # Clear the chat container
    if chat_container is not None:
        chat_container.clear()
    
    # Add a system message
    system_message = f"Agent configuration changed to: {config_name}"
    add_message("system", system_message)
    
    # Update displays
    update_agent_info()
    
    # NEW: Update context display
    if current_agent_config.context_awareness.get("enabled"):
        update_context_display({
            "enabled": True,
            "energy": "ready",
            "confidence": 1.0,
            "adaptation": "Waiting for user input"
        })
    else:
        update_context_display({"enabled": False})

def update_agent_info() -> None:
    """Update the agent information display."""
    global current_agent_config
    
    if current_agent_config:
        agent_info_container.clear()
        
        with agent_info_container:
            ui.label(f"Name: {current_agent_config.name}").classes('font-bold')
            ui.label(f"Description: {current_agent_config.description}")
            ui.label("Personality Traits:").classes('font-bold mt-2')
            
            for trait, value in current_agent_config.personality_traits.items():
                ui.label(f"{trait.capitalize()}: {value:.1f}")
            
            ui.label(f"Expert Domain: {current_agent_config.expert_domain.replace('_', ' ').capitalize()}").classes('font-bold mt-2')
            ui.label(f"Model: {current_agent_config.model_settings.get('model', 'unknown')}").classes('font-bold mt-2')
            ui.label(f"Temperature: {current_agent_config.model_settings.get('temperature', 0.7):.1f}")
            
            # NEW: Show context awareness status
            if current_agent_config.context_awareness.get("enabled"):
                ui.label("🧠 Context Awareness: Enabled").classes('font-bold mt-2 text-green-600')
            else:
                ui.label("🧠 Context Awareness: Disabled").classes('font-bold mt-2 text-gray-500')

def rate_message(message_index: int, rating: int, feedback: str = "") -> None:
    """
    Rate a message.
    
    Args:
        message_index: Index of the message in the conversation
        rating: Rating (1-5)
        feedback: Feedback text
    """
    global messages
    
    if 0 <= message_index < len(messages):
        message = messages[message_index]
        
        if message.get("role") == "assistant":
            # Add evaluation to the message
            message["evaluation"] = {
                "rating": rating,
                "feedback": feedback,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            # Save the evaluation
            evaluation_id = f"{current_conversation_id}_{message_index}"
            evaluation = {
                "conversation_id": current_conversation_id,
                "message_index": message_index,
                "message": message,
                "agent_config": current_agent_config.dict() if current_agent_config else None,
                "rating": rating,
                "feedback": feedback,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            save_evaluation(evaluation_id, evaluation)
            
            # Save the conversation
            save_conversation(current_conversation_id, messages)
            
            # Refresh the chat container
            if chat_container is not None:
                chat_container.clear()
                for msg in messages:
                    with chat_container:
                        format_message(msg)

# Enhanced CSS for context awareness with fixed layout
ui.add_head_html("""
<style>
/* Base layout improvements */
.main-container {
    display: grid;
    grid-template-columns: 1fr;
    grid-template-rows: auto 1fr;
    gap: 1rem;
    padding: 1rem;
    min-height: 100vh;
    background: linear-gradient(135deg, #f1f5f9 0%, #e2e8f0 100%);
    box-sizing: border-box;
}

.content-grid {
    display: flex;
    gap: 1rem;
    height: calc(100vh - 120px);
    min-height: 600px;
    max-width: 1800px;
    margin: 0 auto;
    align-items: stretch;
}

/* Flexible responsive design */
@media (max-width: 1200px) {
    .config-panel {
        width: 280px;
        min-width: 260px;
        max-width: 320px;
    }
    
    .context-panel {
        width: 280px;
        min-width: 240px;
        max-width: 300px;
    }
    
    .chat-area {
        min-width: 350px;
        max-width: 700px;
    }
}

@media (max-width: 900px) {
    .content-grid {
        flex-direction: column;
        height: auto;
        min-height: calc(100vh - 120px);
        gap: 0.75rem;
    }
    
    .config-panel, .context-panel {
        width: 100%;
        min-width: unset;
        max-width: unset;
        height: auto;
        max-height: 300px;
        flex: 0 0 auto;
    }
    
    .chat-area {
        width: 100%;
        min-width: unset;
        max-width: unset;
        height: 500px;
        flex: 1 0 auto;
    }
}

@media (min-width: 1600px) {
    .content-grid {
        max-width: 1800px;
    }
    
    .config-panel {
        width: 350px;
        max-width: 400px;
    }
    
    .context-panel {
        width: 320px;
        max-width: 350px;
    }
}

/* Panel styling improvements */
.config-panel {
    background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    box-shadow: 0 2px 4px -1px rgba(0, 0, 0, 0.1);
    padding: 1.5rem;
    height: 100%;
    overflow-y: auto;
    display: flex;
    flex-direction: column;
    flex: 0 0 auto;
    min-width: 280px;
    max-width: 400px;
    width: 320px;
}

.context-panel {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border-radius: 12px;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    padding: 1.5rem;
    height: 100%;
    overflow-y: auto;
    display: flex;
    flex-direction: column;
    flex: 0 0 auto;
    min-width: 260px;
    max-width: 350px;
    width: 300px;
}

/* Enhanced chat area */
.chat-area {
    background: white;
    border-radius: 12px;
    box-shadow: 0 2px 4px -1px rgba(0, 0, 0, 0.1);
    border: 1px solid #e5e7eb;
    height: 100%;
    display: flex;
    flex-direction: column;
    overflow: hidden;
    flex: 1 1 auto;
    min-width: 400px;
    max-width: 800px;
}

.chat-scroll-container {
    flex: 1;
    overflow-y: auto;
    padding: 1rem;
    background: #f9fafb;
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
}

.chat-input-container {
    flex-shrink: 0;
    background: white;
    border-top: 1px solid #e5e7eb;
    padding: 1rem;
    display: flex;
    gap: 0.75rem;
    align-items: center;
}

/* Header improvements */
.main-header {
    background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%);
    color: white;
    padding: 1rem 1.5rem;
    border-radius: 12px;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    display: flex;
    align-items: center;
    justify-content: space-between;
}

/* Message styling improvements */
.message-card {
    background: white;
    border: 1px solid #e5e7eb;
    border-radius: 8px;
    padding: 1rem;
    box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.1);
    margin-bottom: 0;
}

/* Form improvements */
.input-field {
    border-radius: 8px !important;
    border: 1px solid #d1d5db !important;
    padding: 0.75rem 1rem !important;
    font-size: 1rem !important;
    transition: all 0.2s ease !important;
    flex: 1;
}

.input-field:focus {
    border-color: #3b82f6 !important;
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1) !important;
    outline: none !important;
}

.send-button {
    background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%) !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 0.75rem 1.5rem !important;
    color: white !important;
    font-weight: 600 !important;
    transition: all 0.2s ease !important;
    cursor: pointer !important;
    flex-shrink: 0;
}

.send-button:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
}

/* Agent info styling */
.agent-info-container {
    flex: 1;
    overflow-y: auto;
}

.agent-info-container label {
    display: block;
    margin-bottom: 0.5rem;
    line-height: 1.4;
    word-wrap: break-word;
}

/* Select dropdown improvements */
.agent-select {
    width: 100% !important;
    margin-bottom: 1rem !important;
    border-radius: 8px !important;
    border: 1px solid #d1d5db !important;
    padding: 0.75rem !important;
    background: white !important;
}

/* Context display improvements */
.context-display-container label {
    display: block;
    margin-bottom: 0.75rem;
    line-height: 1.5;
    word-wrap: break-word;
}

/* Scrollbar styling */
.config-panel::-webkit-scrollbar,
.context-panel::-webkit-scrollbar,
.chat-scroll-container::-webkit-scrollbar {
    width: 6px;
}

.config-panel::-webkit-scrollbar-track,
.context-panel::-webkit-scrollbar-track,
.chat-scroll-container::-webkit-scrollbar-track {
    background: rgba(0, 0, 0, 0.1);
    border-radius: 3px;
}

.config-panel::-webkit-scrollbar-thumb,
.context-panel::-webkit-scrollbar-thumb,
.chat-scroll-container::-webkit-scrollbar-thumb {
    background: rgba(0, 0, 0, 0.3);
    border-radius: 3px;
}

.config-panel::-webkit-scrollbar-thumb:hover,
.context-panel::-webkit-scrollbar-thumb:hover,
.chat-scroll-container::-webkit-scrollbar-thumb:hover {
    background: rgba(0, 0, 0, 0.5);
}

/* Ensure no overlapping */
* {
    box-sizing: border-box;
}

/* Fix any potential z-index issues */
.main-header {
    z-index: 10;
}

.config-panel {
    z-index: 1;
}

.chat-area {
    z-index: 1;
}

.context-panel {
    z-index: 1;
}
</style>
""")

# Create the enhanced UI with fixed 3-panel layout
with ui.column().classes('main-container'):
    # Enhanced header
    with ui.row().classes('main-header'):
        ui.label("APL Context-Aware: Sophisticated Agent Platform").classes('text-xl md:text-2xl font-bold')
    
    # Content grid with 3 panels
    with ui.row().classes('content-grid'):
        # Fixed config panel (left side)
        with ui.column().classes('config-panel'):
            ui.label("Agent Configuration").classes('text-xl font-bold mb-4 text-gray-800')
            
            agent_config_select = ui.select(
                options=list_agent_configs(),
                value=list_agent_configs()[0] if list_agent_configs() else None,
                on_change=lambda e: handle_agent_config_change(e.value)
            ).classes('agent-select')
            
            with ui.column().classes('agent-info-container'):
                agent_info_container = ui.column().classes('w-full')
            
            if agent_config_select.value:
                handle_agent_config_change(agent_config_select.value)
        
        # Enhanced main content area - chat interface (middle)
        with ui.column().classes('chat-area'):
            chat_container = ui.column().classes('chat-scroll-container')
            
            with ui.row().classes('chat-input-container'):
                message_input = ui.input(placeholder="Type your message here...").classes('input-field')
                ui.button("Send", on_click=lambda: asyncio.create_task(handle_user_message(message_input.value))).classes('send-button')
            
            message_input.on("keydown.enter", lambda: asyncio.create_task(handle_user_message(message_input.value)))
        
        # Enhanced context awareness panel (right side)
        with ui.column().classes('context-panel'):
            with ui.column().classes('context-display-container'):
                context_display_container = ui.column().classes('w-full')
                # Initialize with placeholder content
                ui.label("Context Awareness").classes('text-lg font-bold mb-3')
                ui.label("Select context-aware learning partner to see energy detection").classes('text-sm opacity-90 leading-relaxed')

def run_app(port=8083):
    """
    Run the enhanced application.
    
    Args:
        port: Port to run the application on
    """
    ui.run(title="APL Context-Aware", port=port)

if __name__ in {"__main__", "__mp_main__"}:
    import argparse
    
    parser = argparse.ArgumentParser(description="Run APL Context-Aware")
    parser.add_argument(
        "--port", "-p",
        type=int,
        default=8083,
        help="Port to run the application on (default: 8083)"
    )
    
    args = parser.parse_args()
    
    config = load_config()
    run_app(port=args.port)
