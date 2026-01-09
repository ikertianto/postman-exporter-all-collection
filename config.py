"""
Configuration module for Postman Exporter
Loads settings from environment variables with fallback defaults
"""
import os
from typing import List
from pathlib import Path
from dotenv import load_dotenv

# Load .env file from the same directory as this script
env_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path)

# Load from environment variables
POSTMAN_API_KEY = os.getenv("POSTMAN_API_KEY", "")

# Export settings
EXPORT_DIR = os.getenv("EXPORT_DIR", "exports")
COLLECTION_OUTPUT_FILE = os.getenv("COLLECTION_OUTPUT_FILE", "merged_collection.json")
ENVIRONMENT_OUTPUT_DIR = os.getenv("ENVIRONMENT_OUTPUT_DIR", "environments")

# Workspace settings
TARGET_WORKSPACES_STR = os.getenv("TARGET_WORKSPACES", "")
TARGET_WORKSPACES: List[str] = [ws.strip() for ws in TARGET_WORKSPACES_STR.split(",") if ws.strip()]

# API settings
REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "30"))
ROOT_FOLDER_NAME = os.getenv("ROOT_FOLDER_NAME", "Postman Collections")

# API endpoints
POSTMAN_API_BASE = "https://api.getpostman.com"

# Headers
def get_headers() -> dict:
    """Get API headers with authentication"""
    if not POSTMAN_API_KEY:
        raise ValueError("POSTMAN_API_KEY is not set. Please set it in .env file or environment variables.")
    
    return {
        "X-Api-Key": POSTMAN_API_KEY
    }
