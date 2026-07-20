from llama_cpp import Llama
from backend.config.settings import (
    AGENT2_MODEL_PATH,
    AGENT2_LOADING_PARAMS
)

print("Loading Shared Gemma 4 E2B...")

shared_gemma4 = Llama(
    model_path=AGENT2_MODEL_PATH,
    **AGENT2_LOADING_PARAMS
)

print("Shared Gemma 4 loaded successfully ✓")


def get_shared_model():
    return shared_gemma4