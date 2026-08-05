#!/usr/bin/env python3
"""
PHANTASM Backend — AI Social Engineering Analyzer
Author: nadirzhon | github.com/nadirzhon/phantasm
"""

import os
import json
from functools import lru_cache

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
import anthropic

app = FastAPI(title="PHANTASM", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])


@lru_cache(maxsize=1)
def get_client() -> anthropic.Anthropic:
    """Lazily construct the Anthropic client.

    Constructing this lazily (instead of at import time) means the module can be
    imported for testing and CI without an API key present. The key is only
    required when an analysis request is actually made.
    """
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError("ANTHROPIC_API_KEY environment variable is not set")
    return anthropic.Anthropic(api_key=api_key)


SYSTEM = """You are a world-class cybersecurity expert specializing in social engineering and phishing detection.
Analyze the provided text for manipulation tactics. Return ONLY valid JSON — no markdown, no preamble.
{
  "risk_score": <0-100>,
  "verdict": "<PHISHING|SUSPICIOUS|LEGITIMATE>",
  "summary": "<one sentence>",
  "attacker_goal": "<what they want>",
  "tactics": [
    {
      "type": "<URGENCY|AUTHORITY|FEAR|SCARCITY|IMPERSONATION|DECEPTION|FAKE_REWARD|CURIOSITY>",
      "phrase": "<exact verbatim phrase from input>",
      "explanation": "<why manipulative>",
      "severity": "<HIGH|MEDIUM|LOW>"
    }
  ],
  "psychological_targets": ["<GREED|FEAR|TRUST|CURIOSITY|PANIC|VANITY>"],
  "red_flags": ["<specific red flags>"],
  "legitimacy_indicators": ["<reasons it might be legit, empty array if none>"]
}"""


class AnalyzeRequest(BaseModel):
    text: str


@app.post("/analyze")
async def analyze(req: AnalyzeRequest):
    if len(req.text) > 10000:
        return JSONResponse({"error": "Text too long (max 10000 chars)"}, status_code=400)

    message = get_client().messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1200,
        system=SYSTEM,
        messages=[{"role": "user", "content": f"Analyze this text:\n\n{req.text}"}],
    )
    raw = message.content[0].text
    clean = raw.replace("```json", "").replace("```", "").strip()
    return json.loads(clean)


@app.get("/health")
def health():
    """Health check — does not require an API key."""
    return {"status": "ok", "model": "claude-sonnet-4-6", "key_configured": bool(os.getenv("ANTHROPIC_API_KEY"))}


@app.get("/")
def index():
    frontend = os.path.join(os.path.dirname(__file__), "..", "frontend", "index.html")
    if os.path.exists(frontend):
        return FileResponse(frontend)
    return JSONResponse({"status": "ok", "endpoints": ["/analyze", "/health"]})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
