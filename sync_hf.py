"""
Automated Deployment Script to Hugging Face Spaces for SI-FOREN.
Repository: alkhrzmy/si-foren
"""
import os
import sys
from pathlib import Path
from huggingface_hub import HfApi, create_repo

BASE_DIR = Path(__file__).resolve().parent

TOKEN_FILE = Path.home() / ".cache" / "huggingface" / "token"
HF_TOKEN = os.getenv("HF_TOKEN") or (TOKEN_FILE.read_text().strip() if TOKEN_FILE.exists() else None)

if not HF_TOKEN:
    print("Error: HF_TOKEN not found in environment or ~/.cache/huggingface/token")
    sys.exit(1)

REPO_ID = "alkhrzmy/si-foren"
REPO_TYPE = "space"

print(f"1. Connecting to Hugging Face Hub as alkhrzmy...")
api = HfApi(token=HF_TOKEN)
user = api.whoami()
print(f"   Authenticated as: {user['name']}")

print(f"2. Ensuring Space '{REPO_ID}' exists with Streamlit SDK...")
try:
    url = create_repo(
        repo_id=REPO_ID,
        repo_type=REPO_TYPE,
        space_sdk="gradio",
        private=False,
        exist_ok=True,
        token=HF_TOKEN
    )
    print(f"   Space ready at: {url}")
except Exception as e:
    print(f"   Notice: {e}")

print(f"3. Uploading clean distribution files from {BASE_DIR}...")
try:
    api.upload_folder(
        folder_path=str(BASE_DIR),
        repo_id=REPO_ID,
        repo_type=REPO_TYPE,
        ignore_patterns=[
            ".git/*",
            "__pycache__/*",
            "*.pyc",
            "*.log",
            "sync_hf.py"
        ],
        commit_message="deploy: publish SI-FOREN B2B Procurement Intelligence production release"
    )
    print("4. Deployment uploaded successfully!")
    print(f"\nLive Public URL: https://huggingface.co/spaces/{REPO_ID}")
except Exception as e:
    print(f"Upload error: {e}")
    sys.exit(1)
