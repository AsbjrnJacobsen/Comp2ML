# File: config.py
import os
from dotenv import load_dotenv

load_dotenv()

LLM_CONFIG = {
    "config_list": [
        {
            "model": os.getenv("MISTRAL_MODEL", "open-mistral-nemo"),
            "api_key": os.getenv("MISTRAL_API_KEY"),
            "base_url": os.getenv("MISTRAL_API_BASE_URL", "https://api.mistral.ai/v1"),
            "api_type": "mistral",
            "api_rate_limit": 0.25,
            "repeat_penalty": 1.1,
            "temperature": 0.0,
            "seed": 42,
            "stream": False,
            "native_tool_calls": True,
            "cache_seed": None,
        }
    ]
}