# APL Context-Aware: Enhanced Agents Patterns Lab

**An experimental evolution of the Agents Patterns Lab to handle sophisticated, context-aware agent profiles.**

## Overview

APL Context-Aware extends the original APL platform to support sophisticated agent profiles that can:

- **Detect user context** (energy levels, session state, emotional indicators)
- **Adapt behavior dynamically** based on detected context
- **Maintain stateful awareness** beyond simple conversation memory
- **Evaluate context-aware capabilities** through specialized metrics

This enhanced version addresses the limitation of the original APL in handling complex agent profiles like learning partners, coaches, and adaptive assistants.

## Key Enhancements

### Context Awareness System

- **Energy Level Detection**: Automatically detects user energy (high/medium/low) from input patterns
- **Behavioral Adaptation**: Adjusts response style, complexity, and suggestions based on context
- **Context Visualization**: Real-time display of detected context for transparency

### Enhanced Agent Architecture

- **Sophisticated Profiles**: Support for multi-dimensional behavioral frameworks
- **Dynamic Prompt Generation**: Context-aware system prompts that adapt in real-time
- **Stateful Memory**: Extended memory systems that track user patterns and preferences

### Advanced Evaluation

- **Context Appropriateness Metrics**: Evaluate how well agents match their responses to detected context
- **Behavioral Consistency**: Measure consistency of adaptations across similar contexts
- **Comparative Analysis**: Side-by-side evaluation of context-aware vs standard agents

## Demonstration Scenario

The primary demo showcases a **Context-Aware Learning Partner** that adapts its teaching approach based on user energy:

- **High Energy**: Suggests challenging system-building tasks, complex projects
- **Medium Energy**: Offers balanced, moderate complexity suggestions  
- **Low Energy**: Provides simple, achievable tasks with minimal cognitive load

## Tech Stack

- **Frontend**: NiceGUI with enhanced context display
- **Agent Framework**: LangChain v0.3 with custom context managers
- **Context Detection**: Pattern-based analysis with extensible framework
- **Storage**: File-based with context state persistence
- **Evaluation**: Custom metrics for context-aware behavior

## Project Structure

```text
├── agent.py                    # Extended agent factory with context support
├── context_manager.py          # NEW: Context detection and management
├── main.py                     # Enhanced UI with context awareness
├── run.py                      # Application entry point
├── utils.py                    # Utility functions and configuration
├── requirements.txt            # Project dependencies
├── config/                     
│   ├── .env                    # API keys and configuration
│   └── .env.example            # Configuration template
├── data/                       
│   ├── agent_configs/          # Agent configuration files
│   └── conversations/          # Conversation history with context
├── docs/                       # NEW: Documentation and methodology
│   └── development_methodology/ # AI-human collaboration framework
├── scripts/                    # NEW: Utility scripts
│   └── setup_agents.py         # Agent configuration setup
└── tests/                      # NEW: Comprehensive test suite
    ├── test_context_manager.py # Context detection tests
    ├── test_integration.py     # End-to-end integration tests
    ├── test_behavioral_adaptation.py # Adaptation framework tests
    └── test_backward_compatibility.py # Compatibility tests
```

## Installation

1. **Clone or copy from original APL**:

   ```bash
   cp -r /Users/chrisdumler/Projects/APL /Users/chrisdumler/Projects/APL-ContextAware
   cd /Users/chrisdumler/Projects/APL-ContextAware
   ```

2. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

3. **Configure API keys**:

   ```bash
   cp config/.env.example config/.env
   # Edit config/.env with your API keys
   ```

## Usage

### Basic Operation

```bash
python main.py --port 8083
```

### Alternative Entry Point

```bash
python run.py --port 8083
```

### Testing

```bash
# Run all tests
python -m pytest tests/

# Run specific test suites
python tests/test_context_manager.py
python tests/test_integration.py
python tests/test_behavioral_adaptation.py
```

### Setup Agent Configurations

```bash
python scripts/setup_agents.py
```

## Context-Aware Features

### Energy Detection

The system automatically detects user energy levels through:

- **Language patterns**: Enthusiastic vs. hesitant language
- **Request complexity**: Ambitious vs. simple task requests
- **Conversation patterns**: Rapid engagement vs. short responses

### Behavioral Adaptation

Agents adapt their responses by adjusting:

- **Complexity level**: Simple tasks for low energy, complex challenges for high energy
- **Response style**: Energetic and direct vs. gentle and supportive
- **Session suggestions**: Appropriate duration and scope for detected energy

### Context Visualization

The enhanced UI displays:

- **Detected Context**: Real-time energy level and confidence
- **Adaptation Reasoning**: Why the agent chose specific behaviors
- **Context History**: Patterns over time for learning insights

## Development Methodology

This project showcases an innovative **AI-Human Collaborative Development Framework** documented in `docs/development_methodology/`:

### Work Request System

- **Structured Sprint Planning**: SLC (Simple, Lovable, Complete) framework
- **Human-in-Loop Checkpoints**: Quality gates with PM validation
- **Time Tracking**: Accurate estimation models for AI coding agents

### Process Documentation

- **Standup Reports**: Regular progress updates from AI coding agents
- **PM Responses**: Human feedback and decision points
- **Retrospective Analysis**: Continuous improvement of methodology

### Quality Assurance

- **Comprehensive Test Suite**: Automated testing for all functionality
- **Backward Compatibility**: Ensures existing features remain functional
- **Integration Testing**: End-to-end workflow validation

## Case Study Applications

This enhanced APL serves as a demonstration of:

1. **Advanced Prompt Engineering**: Dynamic prompt generation based on context
2. **Behavioral AI Systems**: Agents that adapt to user state and needs
3. **AI-Human Collaboration**: Structured methodology for AI coding agent projects
4. **Context-Aware Systems**: Real-time adaptation to user energy and state
5. **Professional Software Development**: Clean architecture and comprehensive testing

## Key Features Implemented

### ✅ Context Detection Core

- Pattern-based energy level detection (high/medium/low)
- 83.3% accuracy on test scenarios
- Confidence scoring and reasoning

### ✅ Behavioral Adaptation Framework  

- Dynamic prompt generation based on detected energy
- Learning partner agent with energy-appropriate responses
- Backward compatibility with existing agent types

### ✅ Professional Development Process

- Structured work request system with SLC framework
- Human-in-loop checkpoints for quality assurance
- Comprehensive documentation and time tracking

### ✅ Production-Ready Structure

- Clean directory organization suitable for portfolio presentation
- Comprehensive test suite with 6 test modules
- Professional documentation and development methodology

## Comparison with Original APL

| Feature | Original APL | APL Context-Aware |
|---------|-------------|-------------------|
| Agent Types | Personality + Domain | Sophisticated, Adaptive Profiles |
| Context Awareness | None | Energy Detection + Behavioral Adaptation |
| Prompt Generation | Static System Prompts | Dynamic, Context-Aware Prompts |
| Evaluation | Basic Rating | Context Appropriateness Metrics |
| Use Cases | Simple Chatbots | Learning Partners, Coaches, Adaptive Assistants |

---

**This project demonstrates the evolution from simple personality-based agents to sophisticated, context-aware AI systems capable of adaptive behavior and meaningful user modeling.**
