import os
from pathlib import Path
from dotenv import load_dotenv

env_path = (
    Path(__file__)
    .resolve()
    .parents[1]
    / ".env"
)

load_dotenv(env_path)

# OpenRouter API
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_BASE_URL = ("https://openrouter.ai/api/v1")

# Nemotron Judge Model
JUDGE_MODEL = ("nvidia/nemotron-3-ultra-550b-a55b:free")

# Judge Configuration
MAX_RETRIES = 3
REQUEST_TIMEOUT = 180
TEMPERATURE = 0.0
TOP_P = 1.0

# Metric Names
METRICS = [
    "relevance",
    "clarity",
    "completeness",
    "actionability",
    "structure",
    "depth"
]