"""
Utility functions for APL Context-Aware.

Extended utility functions that include context state management
and enhanced data processing for sophisticated agent profiles.
"""

import os
import json
import logging
from pathlib import Path
from typing import Any, Dict, List, Optional
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Constants
PROJECT_ROOT = Path(__file__).parent
DATA_DIR = PROJECT_ROOT / "data"
CONFIG_DIR = PROJECT_ROOT / "config"
DOCS_DIR = PROJECT_ROOT / "docs"

def load_config() -> Dict[str, str]:
    """
    Load configuration from .env file.
    
    Returns:
        Dict[str, str]: Dictionary containing configuration values
    """
    env_path = CONFIG_DIR / ".env"
    load_dotenv(env_path)
    
    # Set log level based on environment variable
    log_level = os.getenv("LOG_LEVEL", "INFO")
    logging.getLogger().setLevel(getattr(logging, log_level))
    
    logger.info(f"Configuration loaded from {env_path}")
    return dict(os.environ)

def save_json(data: Any, filepath: Path) -> None:
    """
    Save data to a JSON file.
    
    Args:
        data: Data to save
        filepath: Path to save the file
    """
    filepath.parent.mkdir(parents=True, exist_ok=True)
    
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)
    
    logger.debug(f"Data saved to {filepath}")

def load_json(filepath: Path) -> Any:
    """
    Load data from a JSON file.
    
    Args:
        filepath: Path to the file
        
    Returns:
        Any: Loaded data
        
    Raises:
        FileNotFoundError: If the file does not exist
    """
    if not filepath.exists():
        logger.error(f"File not found: {filepath}")
        raise FileNotFoundError(f"File not found: {filepath}")
    
    with open(filepath, "r") as f:
        data = json.load(f)
    
    logger.debug(f"Data loaded from {filepath}")
    return data

def ensure_directory(directory: Path) -> None:
    """
    Ensure that a directory exists.
    
    Args:
        directory: Directory path
    """
    directory.mkdir(parents=True, exist_ok=True)
    logger.debug(f"Ensured directory exists: {directory}")

# Original functions maintained for compatibility
def get_conversation_path(conversation_id: str) -> Path:
    return DATA_DIR / "conversations" / f"{conversation_id}.json"

def save_conversation(conversation_id: str, messages: List[Dict[str, Any]]) -> None:
    conversation_path = get_conversation_path(conversation_id)
    ensure_directory(conversation_path.parent)
    save_json(messages, conversation_path)
    logger.info(f"Conversation saved: {conversation_id}")

def load_conversation(conversation_id: str) -> List[Dict[str, Any]]:
    conversation_path = get_conversation_path(conversation_id)
    try:
        return load_json(conversation_path)
    except FileNotFoundError:
        logger.warning(f"Conversation not found: {conversation_id}")
        return []

def get_agent_config_path(config_name: str) -> Path:
    return DATA_DIR / "agent_configs" / f"{config_name}.json"

def save_agent_config(config_name: str, config: Dict[str, Any]) -> None:
    config_path = get_agent_config_path(config_name)
    ensure_directory(config_path.parent)
    save_json(config, config_path)
    logger.info(f"Agent configuration saved: {config_name}")

def load_agent_config(config_name: str) -> Optional[Dict[str, Any]]:
    config_path = get_agent_config_path(config_name)
    try:
        return load_json(config_path)
    except FileNotFoundError:
        logger.warning(f"Agent configuration not found: {config_name}")
        return None

def list_agent_configs() -> List[str]:
    config_dir = DATA_DIR / "agent_configs"
    ensure_directory(config_dir)
    
    config_files = list(config_dir.glob("*.json"))
    return [config_file.stem for config_file in config_files]

def get_evaluation_path(evaluation_id: str) -> Path:
    return DATA_DIR / "evaluations" / f"{evaluation_id}.json"

def save_evaluation(evaluation_id: str, evaluation: Dict[str, Any]) -> None:
    evaluation_path = get_evaluation_path(evaluation_id)
    ensure_directory(evaluation_path.parent)
    save_json(evaluation, evaluation_path)
    logger.info(f"Evaluation saved: {evaluation_id}")

def load_evaluation(evaluation_id: str) -> Optional[Dict[str, Any]]:
    evaluation_path = get_evaluation_path(evaluation_id)
    try:
        return load_json(evaluation_path)
    except FileNotFoundError:
        logger.warning(f"Evaluation not found: {evaluation_id}")
        return None

# NEW: Context state management functions
def get_context_state_path(conversation_id: str) -> Path:
    """Get the path for a context state file."""
    return DATA_DIR / "context_states" / f"{conversation_id}.json"

def save_context_state(conversation_id: str, context_state: Dict[str, Any]) -> None:
    """Save context state for a conversation."""
    state_path = get_context_state_path(conversation_id)
    ensure_directory(state_path.parent)
    save_json(context_state, state_path)
    logger.debug(f"Context state saved: {conversation_id}")

def load_context_state(conversation_id: str) -> Dict[str, Any]:
    """Load context state for a conversation."""
    state_path = get_context_state_path(conversation_id)
    try:
        return load_json(state_path)
    except FileNotFoundError:
        logger.debug(f"Context state not found, creating new: {conversation_id}")
        return {
            "energy_history": [],
            "behavioral_patterns": {},
            "user_preferences": {},
            "session_count": 0
        }

def get_context_profile_path(profile_name: str) -> Path:
    """Get the path for a context detection profile."""
    return DATA_DIR / "context_profiles" / f"{profile_name}.json"

def save_context_profile(profile_name: str, profile: Dict[str, Any]) -> None:
    """Save a context detection profile."""
    profile_path = get_context_profile_path(profile_name)
    ensure_directory(profile_path.parent)
    save_json(profile, profile_path)
    logger.info(f"Context profile saved: {profile_name}")

def load_context_profile(profile_name: str) -> Optional[Dict[str, Any]]:
    """Load a context detection profile."""
    profile_path = get_context_profile_path(profile_name)
    try:
        return load_json(profile_path)
    except FileNotFoundError:
        logger.warning(f"Context profile not found: {profile_name}")
        return None