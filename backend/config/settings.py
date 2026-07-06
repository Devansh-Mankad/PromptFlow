import os
ENV = os.getenv("ENV", "development")

# Model Path
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

AGENT1_MODEL_PATH = os.path.join(BASE_DIR, "models", "agent1.gguf")
AGENT2_MODEL_PATH = os.path.join(BASE_DIR, "models", "agent2.gguf")

AGENT1_LOADING_PARAMS = {
    # Context window size for the model
    "n_ctx": 2048,
    # Number of CPU threads used for inference
    "n_threads": 4,
    # Number of tokens processed in one batch
    "n_batch": 128,
    # Disable model loading logs for cleaner output
    "verbose": False,
}

AGENT1_INFERENCE_PARAMS = {
    # Maximum output length (approx. 180-200 words)
    "max_tokens": 768,
    # Controls output randomness
    "temperature": 0.4,
    # Uses high-probability token choices for reliable outputs
    "top_p": 0.9,
    # Limits token selection to the top 40 likely candidates
    "top_k": 40,
    # Slightly reduces repetition in generated text
    "repeat_penalty": 1.1,
    # Stop generation when these tokens are encountered
    "stop": ["<end_of_turn>"],
    # Return only generated text, not the input prompt
    "echo": False,
}

AGENT2_LOADING_PARAMS = {
    # Context window size for the model (larger as produce response)
    "n_ctx": 4096,
    # Number of CPU threads used for inference
    "n_threads": 4,
    # Number of tokens processed in one batch
    "n_batch": 128,
    # Disable model loading logs for cleaner output
    "verbose": False,
}

AGENT2_INFERENCE_PARAMS = {
    # Maximum output length (approx. 700-800 words)
    "max_tokens": 2048,
    # Controls output randomness; 0.7 provides a balance between consistency and creativity
    "temperature": 0.7,
    # Uses high-probability token choices for reliable outputs
    "top_p": 0.90,
    # Limits token selection to the top 40 likely candidates
    "top_k": 40,
    # Slightly reduces repetition in generated text
    "repeat_penalty": 1.15,
    # Stop generation when these tokens are encountered
    "stop": ["<end_of_turn>"],
    # Return only generated text, not the input prompt
    "echo": False,
}