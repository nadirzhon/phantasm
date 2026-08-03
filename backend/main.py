#!/usr/bin/env python3
"""
PHANTASM Backend — AI Social Engineering Analyzer
Author: nadirzhon | github.com/nadirzhon/phantasm
"""

import os
import json
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import anthropic

app = FastAPI(title="PHANTASM", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])

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
        return {"error": "Text too long (max 10000 chars)"}
    
    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1200,
        system=SYSTEM,
        messages=[{"role": "user", "content": f"Analyze this text:\n\n{req.text}"}]
    )
    raw = message.content[0].text
    clean = raw.replace("```json", "").replace("```", "").strip()
    return json.loads(clean)

@app.get("/health")
def health():
    return {"status": "ok", "model": "claude-sonnet-4-6"}

@app.get("/")
def index():
    return FileResponse("../frontend/index.html")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
