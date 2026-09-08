"""
LLM Client Interface for SI-FOREN.
Primary: Hugging Face Serverless Inference API (Qwen/Qwen2.5-72B-Instruct) using HF Token.
Fallback: Local Antigravity CLIProxyAPI (if available locally).
"""
import os
import json
from pathlib import Path
from typing import Any, Dict, List, Optional
import requests
from huggingface_hub import InferenceClient

HF_TOKEN_FILE = Path.home() / ".cache" / "huggingface" / "token"


def get_default_hf_token() -> Optional[str]:
    token = os.getenv("HF_TOKEN") or os.getenv("HUGGINGFACE_API_TOKEN")
    if not token:
        try:
            import streamlit as st
            token = st.secrets.get("HF_TOKEN") or st.secrets.get("HUGGINGFACE_API_TOKEN")
        except Exception:
            pass
    if not token and HF_TOKEN_FILE.exists():
        try:
            token = HF_TOKEN_FILE.read_text().strip()
        except Exception:
            pass
    return token


class LLMClient:
    def __init__(
        self,
        hf_token: Optional[str] = None,
        hf_model: str = "Qwen/Qwen2.5-72B-Instruct",
        base_url: Optional[str] = None,
        api_key: Optional[str] = None,
        model: Optional[str] = None
    ):
        self.hf_token = hf_token or get_default_hf_token()
        self.hf_model = hf_model
        
        self.base_url = (base_url or os.getenv("LLM_BASE_URL", "http://127.0.0.1:8317/v1")).rstrip("/")
        self.api_key = api_key or os.getenv("LLM_API_KEY", "sora-hermes-proxy-2026")
        self.fallback_model = model or os.getenv("LLM_MODEL", "gemini-3.7-flash-high")
        
        self.hf_client = InferenceClient(token=self.hf_token) if self.hf_token else None

    def call_reasoning(self, system_prompt: str, user_prompt: str, temperature: float = 0.1, max_tokens: int = 2000) -> str:
        """
        Executes reasoning pass via Hugging Face Qwen/Qwen2.5-72B-Instruct first,
        with seamless fallback to local proxy if HF is busy or times out.
        """
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]

        # 1. Try Hugging Face Serverless API first (Qwen/Qwen2.5-72B-Instruct)
        if self.hf_client:
            try:
                res = self.hf_client.chat_completion(
                    messages=messages,
                    model=self.hf_model,
                    max_tokens=max_tokens,
                    temperature=temperature
                )
                if res.choices and res.choices[0].message and res.choices[0].message.content:
                    return res.choices[0].message.content
            except Exception:
                pass

        # 2. Fallback to Local Proxy (if running locally)
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": self.fallback_model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        try:
            resp = requests.post(f"{self.base_url}/chat/completions", headers=headers, json=payload, timeout=45)
            if resp.status_code == 200:
                data = resp.json()
                return data["choices"][0]["message"]["content"]
            else:
                raise RuntimeError(f"Proxy status {resp.status_code}: {resp.text}")
        except Exception as e:
            raise RuntimeError(f"All LLM backends failed: {e}")
