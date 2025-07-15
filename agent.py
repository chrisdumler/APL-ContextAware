"""
Agent implementation for APL Context-Aware.

Extended from original APL to support context-aware agent configurations
and sophisticated behavioral patterns.
"""

import uuid
from typing import Any, Dict, List, Optional, Tuple
from pydantic import BaseModel, Field

from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder # type: ignore
from langchain.schema.runnable import RunnablePassthrough, RunnableLambda
from langchain.schema.messages import AIMessage, HumanMessage, SystemMessage
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain.memory import ConversationBufferMemory
from langchain_openai import ChatOpenAI

from utils import logger, load_agent_config, save_agent_config

# Define personality traits and their descriptions
PERSONALITY_TRAITS = {
    "formality": {
        "description": "How formal or casual the agent's responses are",
        "low": "casual, relaxed, using contractions and colloquialisms",
        "high": "formal, professional, using proper grammar and vocabulary"
    },
    "verbosity": {
        "description": "How detailed or concise the agent's responses are",
        "low": "concise, to-the-point, focusing on key information",
        "high": "detailed, thorough, providing comprehensive explanations"
    },
    "creativity": {
        "description": "How creative or conservative the agent's responses are",
        "low": "conservative, factual, sticking to established information",
        "high": "creative, imaginative, exploring novel ideas and connections"
    }
}

# Define expert domains and their descriptions
EXPERT_DOMAINS = {
    "technical_writer": {
        "description": "Specializes in clear, precise technical documentation",
        "skills": ["technical writing", "documentation", "explanation", "clarity"]
    },
    "customer_support": {
        "description": "Specializes in helpful, empathetic customer assistance",
        "skills": ["problem solving", "empathy", "clarity", "assistance"]
    },
    "creative_collaborator": {
        "description": "Specializes in creative brainstorming and idea generation",
        "skills": ["creativity", "brainstorming", "idea generation", "collaboration"]
    },
    "data_analyst": {
        "description": "Specializes in data analysis and interpretation",
        "skills": ["data analysis", "interpretation", "pattern recognition", "explanation"]
    },
    "learning_partner": {
        "description": "Specializes in adaptive learning support and coding mentorship",
        "skills": ["teaching", "adaptation", "mentorship", "technical guidance"]
    }
}

class AgentConfig(BaseModel):
    """Configuration for an agent."""
    
    # Basic information
    name: str = Field(..., description="Name of the agent configuration")
    description: str = Field("", description="Description of the agent configuration")
    
    # Personality traits (0.0 to 1.0)
    personality_traits: Dict[str, float] = Field(
        default_factory=lambda: {
            "formality": 0.5,
            "verbosity": 0.5,
            "creativity": 0.5
        },
        description="Personality traits of the agent (0.0 to 1.0)"
    )
    
    # Expert domain
    expert_domain: str = Field(
        "technical_writer",
        description="Expert domain of the agent"
    )
    
    # Memory settings
    memory_settings: Dict[str, Any] = Field(
        default_factory=lambda: {
            "history_length": 10,
            "summarize_after": 20
        },
        description="Memory settings for the agent"
    )
    
    # Model settings
    model_settings: Dict[str, Any] = Field(
        default_factory=lambda: {
            "model": "gpt-4",
            "temperature": 0.7
        },
        description="Model settings for the agent"
    )
    
    # NEW: Context awareness settings
    context_awareness: Dict[str, Any] = Field(
        default_factory=lambda: {
            "enabled": False,
            "energy_detection": True,
            "behavioral_adaptation": True
        },
        description="Context awareness settings"
    )
    
    model_config = {
        "arbitrary_types_allowed": True,
        "protected_namespaces": ()
    }

class AgentFactory:
    """Factory for creating agents with different configurations."""
    
    def __init__(self):
        """Initialize the agent factory."""
        self.default_config = AgentConfig(
            name="default",
            description="Default agent configuration"
        )
    
    def _build_system_prompt(self, config: AgentConfig, user_energy: str = None) -> str:
        """
        Build the system prompt for the agent based on the configuration and user energy.
        
        Args:
            config: Agent configuration
            user_energy: Detected user energy level (high/medium/low) for behavioral adaptation
            
        Returns:
            str: System prompt adapted for user energy level
        """
        # Get personality trait descriptions
        personality_desc = []
        for trait, value in config.personality_traits.items():
            if trait in PERSONALITY_TRAITS:
                trait_info = PERSONALITY_TRAITS[trait]
                # Determine if the trait is more towards low or high
                if value < 0.4:
                    trait_desc = f"Your {trait} is low: {trait_info['low']}"
                elif value > 0.6:
                    trait_desc = f"Your {trait} is high: {trait_info['high']}"
                else:
                    trait_desc = f"Your {trait} is balanced between {trait_info['low']} and {trait_info['high']}"
                personality_desc.append(trait_desc)
        
        # Get expert domain description
        domain_desc = ""
        if config.expert_domain in EXPERT_DOMAINS:
            domain_info = EXPERT_DOMAINS[config.expert_domain]
            domain_desc = f"You are a {config.expert_domain.replace('_', ' ')}: {domain_info['description']}.\n"
            domain_desc += f"Your key skills include: {', '.join(domain_info['skills'])}."
        
        # Build energy-based adaptation if context awareness is enabled
        energy_adaptation = ""
        if (config.context_awareness.get("enabled") and 
            config.context_awareness.get("behavioral_adaptation") and 
            user_energy and 
            config.expert_domain == "learning_partner"):
            
            energy_adaptation = self._get_energy_adaptation(user_energy)
        
        # Build the complete system prompt
        system_prompt = f"""You are an AI assistant named {config.name}.
        
{domain_desc}

Your personality traits:
{chr(10).join(f"- {trait}" for trait in personality_desc)}

{energy_adaptation}

Always maintain these traits in your responses. Your goal is to provide helpful, accurate, and appropriate responses to the user's queries.

Remember to:
1. Answer questions truthfully based on the information available to you
2. Admit when you don't know something
3. Provide reasoning for your answers when appropriate
4. Maintain a consistent personality throughout the conversation
"""
        
        return system_prompt
    
    def _get_energy_adaptation(self, user_energy: str) -> str:
        """
        Generate energy-specific behavioral adaptation for learning partner.
        
        Args:
            user_energy: Detected user energy level (high/medium/low)
            
        Returns:
            str: Energy-specific adaptation instructions
        """
        adaptations = {
            "high": """
ENERGY ADAPTATION - High Energy User Detected:
Your user is energetic and motivated! Adapt your response style accordingly:

• Suggest challenging, complex tasks and projects
• Use an enthusiastic, energetic tone that matches their excitement
• Recommend 20-30 minute session types (SYSTEM, INTEGRATE) 
• Offer ambitious solutions and comprehensive approaches
• Example responses: "Excellent energy! Want to build a complete system for automating evaluation runs across multiple models?"

Session Types to Suggest:
- SYSTEM: Building complete systems and architectures
- INTEGRATE: Complex integration projects
- DEEP_DIVE: Thorough exploration of advanced topics
""",
            "medium": """
ENERGY ADAPTATION - Medium Energy User Detected:
Your user has steady, balanced energy. Adapt your response style accordingly:

• Suggest moderate complexity tasks with clear value
• Use an informative, steady tone that builds confidence
• Recommend 15-20 minute session types (AUTOMATE, VISUALIZE)
• Offer practical, achievable solutions
• Example responses: "Great! Should we create a practical dashboard for visualizing your evaluation results?"

Session Types to Suggest:
- AUTOMATE: Practical automation solutions
- VISUALIZE: Data visualization and analysis
- OPTIMIZE: Improving existing code and processes
""",
            "low": """
ENERGY ADAPTATION - Low Energy User Detected:
Your user has gentle, cautious energy. Adapt your response style accordingly:

• Suggest simple, immediately achievable tasks
• Use a gentle, supportive tone that encourages small wins
• Recommend 10-15 minute session types (quick utilities)
• Offer bite-sized, manageable solutions
• Example responses: "No worries! Want to create a small utility script to help with evaluation data formatting? We can keep it simple."

Session Types to Suggest:
- UTILITY: Small helper scripts and tools
- CLEANUP: Simple code organization tasks  
- EXPLORE: Gentle exploration of concepts
"""
        }
        
        return adaptations.get(user_energy, "")
    
    def _setup_memory(self, config: AgentConfig) -> ConversationBufferMemory:
        """
        Set up the memory for the agent based on the configuration.
        
        Args:
            config: Agent configuration
            
        Returns:
            ConversationBufferMemory: Memory for the agent
        """
        return ConversationBufferMemory(
            chat_memory=ChatMessageHistory(),
            return_messages=True,
            memory_key="chat_history",
            output_key="output"
        )
    
    def _setup_model(self, config: AgentConfig) -> ChatOpenAI:
        """
        Set up the model for the agent based on the configuration.
        
        Args:
            config: Agent configuration
            
        Returns:
            ChatOpenAI: Model for the agent
        """
        return ChatOpenAI(
            model=config.model_settings.get("model", "gpt-4"),
            temperature=config.model_settings.get("temperature", 0.7)
        )
    
    def create_agent(self, config_name: str = None, user_energy: str = None) -> Tuple[Any, AgentConfig]:
        """
        Create an agent with the specified configuration and optional energy context.
        
        Args:
            config_name: Name of the configuration to use (default: None, uses default config)
            user_energy: Detected user energy level for behavioral adaptation
            
        Returns:
            Tuple[Any, AgentConfig]: Tuple containing the agent chain and the configuration
        """
        # Load the configuration or use the default
        if config_name:
            config_dict = load_agent_config(config_name)
            if config_dict:
                config = AgentConfig(**config_dict)
                logger.info(f"Loaded agent configuration: {config_name}")
            else:
                logger.warning(f"Configuration not found: {config_name}, using default")
                config = self.default_config
        else:
            config = self.default_config
        
        # Set up the memory
        memory = self._setup_memory(config)
        
        # Set up the model
        model = self._setup_model(config)
        
        # Build the prompt with energy context
        system_prompt = self._build_system_prompt(config, user_energy)
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}")
        ])
        
        # Build the chain
        chain = (
            RunnablePassthrough.assign(
                chat_history=lambda x: memory.load_memory_variables({})["chat_history"]
            )
            | prompt
            | model
            | RunnableLambda(lambda x: {"output": x.content})
        )
        
        # Create a function to handle both chain execution and memory updating
        def run_chain_with_memory(inputs):
            # Run the chain
            outputs = chain.invoke(inputs)
            
            # Update memory
            memory.save_context(
                {"input": inputs["input"]},
                {"output": outputs["output"]}
            )
            
            return outputs
        
        # Use RunnableLambda instead of hooks for memory management
        chain_with_memory = RunnableLambda(run_chain_with_memory)
        
        return chain_with_memory, config
    
    def create_agent_from_config(self, config: AgentConfig, user_energy: str = None) -> Any:
        """
        Create an agent from an AgentConfig object directly.
        
        Args:
            config: AgentConfig object to use
            user_energy: Detected user energy level for behavioral adaptation
            
        Returns:
            Agent chain ready for invocation
        """
        # Set up the memory
        memory = self._setup_memory(config)
        
        # Set up the model
        model = self._setup_model(config)
        
        # Build the prompt with energy context
        system_prompt = self._build_system_prompt(config, user_energy)
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}")
        ])
        
        # Build the chain
        chain = (
            RunnablePassthrough.assign(
                chat_history=lambda x: memory.load_memory_variables({})["chat_history"]
            )
            | prompt
            | model
            | RunnableLambda(lambda x: {"output": x.content})
        )
        
        # Create a function to handle both chain execution and memory updating
        def run_chain_with_memory(inputs):
            # Run the chain
            outputs = chain.invoke(inputs)
            
            # Update memory
            memory.save_context(
                {"input": inputs["input"]},
                {"output": outputs["output"]}
            )
            
            return outputs
        
        # Use RunnableLambda instead of hooks for memory management
        chain_with_memory = RunnableLambda(run_chain_with_memory)
        
        return chain_with_memory
    
    def save_config(self, config: AgentConfig) -> None:
        """
        Save an agent configuration.
        
        Args:
            config: Agent configuration to save
        """
        save_agent_config(config.name, config.dict())
        logger.info(f"Saved agent configuration: {config.name}")
    
    def create_default_configs(self) -> List[str]:
        """
        Create default agent configurations.
        
        Returns:
            List[str]: List of created configuration names
        """
        configs = []
        
        # Formal technical writer
        formal_tech_writer = AgentConfig(
            name="formal_technical_writer",
            description="A formal technical writer focused on clear documentation",
            personality_traits={
                "formality": 0.8,
                "verbosity": 0.7,
                "creativity": 0.3
            },
            expert_domain="technical_writer",
            model_settings={
                "model": "gpt-4",
                "temperature": 0.3
            }
        )
        self.save_config(formal_tech_writer)
        configs.append(formal_tech_writer.name)
        
        # Casual customer support
        casual_support = AgentConfig(
            name="casual_customer_support",
            description="A casual, friendly customer support agent",
            personality_traits={
                "formality": 0.3,
                "verbosity": 0.5,
                "creativity": 0.6
            },
            expert_domain="customer_support",
            model_settings={
                "model": "gpt-4",
                "temperature": 0.7
            }
        )
        self.save_config(casual_support)
        configs.append(casual_support.name)
        
        # Creative collaborator
        creative_collaborator = AgentConfig(
            name="creative_collaborator",
            description="A highly creative collaborator for brainstorming",
            personality_traits={
                "formality": 0.4,
                "verbosity": 0.7,
                "creativity": 0.9
            },
            expert_domain="creative_collaborator",
            model_settings={
                "model": "gpt-4",
                "temperature": 0.9
            }
        )
        self.save_config(creative_collaborator)
        configs.append(creative_collaborator.name)
        
        # Data analyst
        data_analyst = AgentConfig(
            name="data_analyst",
            description="A precise, analytical data interpreter",
            personality_traits={
                "formality": 0.6,
                "verbosity": 0.8,
                "creativity": 0.4
            },
            expert_domain="data_analyst",
            model_settings={
                "model": "gpt-4",
                "temperature": 0.2
            }
        )
        self.save_config(data_analyst)
        configs.append(data_analyst.name)
        
        # NEW: Context-aware learning partner
        learning_partner = AgentConfig(
            name="context_aware_learning_partner",
            description="An adaptive learning partner that adjusts to user energy and context",
            personality_traits={
                "formality": 0.4,
                "verbosity": 0.6,
                "creativity": 0.7
            },
            expert_domain="learning_partner",
            context_awareness={
                "enabled": True,
                "energy_detection": True,
                "behavioral_adaptation": True
            },
            model_settings={
                "model": "gpt-4",
                "temperature": 0.7
            }
        )
        self.save_config(learning_partner)
        configs.append(learning_partner.name)
        
        logger.info(f"Created {len(configs)} default agent configurations")
        return configs