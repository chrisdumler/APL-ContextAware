# APL Context-Aware: Enhanced Agents Patterns Lab

**Evolution of the Agents Patterns Lab to handle sophisticated, context-aware agent profiles.**

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
├── main.py                     # Enhanced UI with context awareness
├── agent.py                    # Extended agent factory with context support
├── context_manager.py          # NEW: Context detection and management
├── adaptive_behavior.py        # NEW: Behavioral adaptation framework
├── evaluation/                 # NEW: Context-aware evaluation tools
│   ├── context_metrics.py      # Context appropriateness measurement
│   └── comparative_analysis.py # A/B testing framework
├── config/                     
│   └── .env                    # API keys and configuration
├── data/                       
│   ├── agent_configs/          # Agent configuration files
│   ├── conversations/          # Conversation history with context
│   ├── evaluations/            # Evaluation results
│   └── context_profiles/       # NEW: Context detection profiles
└── demos/                      # NEW: Demonstration scenarios
    ├── learning_partner.py     # Primary demo implementation
    └── comparison_demo.py      # Side-by-side comparison
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
python run.py --port 8083
```

### Demo Mode

```bash
python demos/learning_partner.py
```

### Comparison Mode

```bash
python demos/comparison_demo.py
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

## Evaluation Framework

### Context Appropriateness Metrics

- **Energy Match Score**: How well response complexity matches detected energy
- **Adaptation Consistency**: Reliability of behavioral changes
- **User Satisfaction**: Preference ratings for context-aware vs. standard responses

### Comparative Analysis

- **A/B Testing**: Direct comparison between context-aware and standard agents
- **Performance Metrics**: Task completion, engagement, satisfaction
- **Behavioral Analytics**: Patterns in context detection and adaptation

## Case Study Applications

This enhanced APL serves as a demonstration of:

1. **Advanced Prompt Engineering**: Dynamic prompt generation based on context
2. **Behavioral AI Systems**: Agents that adapt to user state and needs
3. **Evaluation Methodology**: Frameworks for measuring sophisticated AI behaviors
4. **Human-AI Interaction**: Context-aware systems that feel more intelligent and responsive

## Future Enhancements

- **Multi-dimensional Context**: Emotion, expertise level, time constraints
- **Machine Learning Integration**: Trained context detection models
- **External Context Sources**: Calendar integration, biometric data
- **Advanced Memory Systems**: Long-term user modeling and preferences

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
