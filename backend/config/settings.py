# from huggingface_hub import hf_hub_download

# # AGENT1_REPO_ID = "mankadevansh/promptflow-agents"
# # AGENT1_FILENAME = "agent1_gemma.gguf"

# AGENT2_REPO_ID = "mankadevansh/promptflow-agents"
# AGENT2_FILENAME = "agent2.gguf"

# # AGENT1_MODEL_PATH = hf_hub_download(
# #     repo_id=AGENT1_REPO_ID,
# #     filename=AGENT1_FILENAME
# # )

# AGENT2_MODEL_PATH = hf_hub_download(
#     repo_id=AGENT2_REPO_ID,
#     filename=AGENT2_FILENAME
# )

# import os
# ENV = os.getenv("ENV", "development")

# # Model Path
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# AGENT1_MODEL_PATH = os.path.join(BASE_DIR, "models", "c:/Users/devan/Downloads/gemma-3-1b-it.Q4_K_M (4).gguf")
# # AGENT2_MODEL_PATH = os.path.join(BASE_DIR, "models", "agent2.gguf")

# AGENT1_LOADING_PARAMS = {
#     # Context window size for the model
#     "n_ctx": 4096,
#     # Number of CPU threads used for inference
#     "n_threads": 4,
#     # Number of tokens processed in one batch
#     "n_batch": 128,
#     # Disable model loading logs for cleaner output
#     "verbose": False,
# }

# AGENT1_INFERENCE_PARAMS = {
#     "max_tokens": 480,
#     "temperature": 0.20,
#     "top_p": 0.90,
#     "top_k": 40,
#     "min_p": 0.05,
#     "repeat_penalty": 1.10,
#     "stop": ["<end_of_turn>", "<eos>"],
#     "echo": False,
# }

# AGENT2_LOADING_PARAMS = {
#     # Context window size for the model (larger as produce response)
#     "n_ctx": 4096,
#     # Number of CPU threads used for inference
#     "n_threads": 4,
#     # Number of tokens processed in one batch
#     "n_batch": 128,
#     # Disable model loading logs for cleaner output
#     "verbose": False,
# }

# AGENT2_INFERENCE_PARAMS = {
#     "max_tokens": 3072,
#     "temperature": 0.0,
#     "top_p": 1.0,
#     "top_k": 0,
#     "repeat_penalty": 1.0,
#     "stop": ["<end_of_turn>", "<eos>"],
#     "echo": False,
# }

# Agent 1:
AGENT1_OLLAMA_MODEL = "promptflow_gemma3"

# Agent 2 + Raw Agent:
AGENT2_OLLAMA_MODEL = "promptflow_gemma4"
OLLAMA_HOST = "http://localhost:11434"