"""
Setup script to create default agent configurations.

This ensures the context-aware learning partner is available for testing.
"""

from agent import AgentFactory
from utils import ensure_directory
from pathlib import Path

def setup_default_agents():
    """Create default agent configurations including context-aware learning partner."""
    
    # Ensure data directory exists
    data_dir = Path("data")
    ensure_directory(data_dir)
    
    # Create agent factory and generate default configs
    factory = AgentFactory()
    configs = factory.create_default_configs()
    
    print("=== Agent Configuration Setup ===")
    print(f"Created {len(configs)} default agent configurations:")
    
    for config_name in configs:
        print(f"  ✅ {config_name}")
    
    print(f"\n✅ All agent configurations ready!")
    print("Available for use in the UI application.")

if __name__ == "__main__":
    setup_default_agents()