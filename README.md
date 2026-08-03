<div align="center">

```
██████╗ ██╗  ██╗ █████╗ ███╗   ██╗████████╗ █████╗ ███████╗███╗   ███╗
██╔══██╗██║  ██║██╔══██╗████╗  ██║╚══██╔══╝██╔══██╗██╔════╝████╗ ████║
██████╔╝███████║███████║██╔██╗ ██║   ██║   ███████║███████╗██╔████╔██║
██╔═══╝ ██╔══██║██╔══██║██║╚██╗██║   ██║   ██╔══██║╚════██║██║╚██╔╝██║
██║     ██║  ██║██║  ██║██║ ╚████║   ██║   ██║  ██║███████║██║ ╚═╝ ██║
╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═══╝   ╚═╝   ╚═╝  ╚═╝╚══════╝╚═╝     ╚═╝
```

**AI-powered social engineering & phishing analyzer**

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=flat-square&logo=python&logoColor=white)](https://python.org)
[![Claude](https://img.shields.io/badge/Claude-Sonnet_4.6-FF6B35?style=flat-square)](https://anthropic.com)
[![React](https://img.shields.io/badge/React-18-61DAFB?style=flat-square&logo=react&logoColor=black)](https://react.dev)
[![License](https://img.shields.io/badge/License-MIT-yellow?style=flat-square)](LICENSE)

*Paste any suspicious message. Watch AI dissect every manipulation tactic in real time.*

</div>

---

## What it does

PHANTASM uses Claude AI to analyze any text — phishing emails, scam SMS, social engineering messages — and produces a color-coded **manipulation map** with:

- **Risk score** (0–100) and verdict: PHISHING / SUSPICIOUS / LEGITIMATE
- **Color-highlighted tactics** in the original text — hover any highlight to see exactly why it's manipulative
- **Psychological breakdown** — what emotions the attacker is targeting (FEAR, GREED, URGENCY, TRUST...)
- **Attacker goal** — what action they want you to take
- **Red flags** — specific technical and contextual indicators

## Detected tactics

| Tactic | Description |
|--------|-------------|
| `URGENCY` | Artificial time pressure — "act NOW", "24 hours remaining" |
| `AUTHORITY` | False authority claims — impersonating banks, government, tech giants |
| `FEAR` | Threats of negative consequences — suspension, legal action, data loss |
| `SCARCITY` | Limited availability framing — "your last chance", "final notice" |
| `IMPERSONATION` | Pretending to be a trusted brand or person |
| `DECEPTION` | Outright lies and false claims |
| `FAKE_REWARD` | Bogus prize or reward to lure action |
| `CURIOSITY` | Exploiting curiosity to induce clicks |

## Quick Start

### Docker
```bash
git clone https://github.com/nadirzhon/phantasm
cd phantasm
ANTHROPIC_API_KEY=your_key docker compose up
open http://localhost:3000
```

### Manual
```bash
cd backend && pip install -r requirements.txt
ANTHROPIC_API_KEY=your_key python main.py
# In another terminal:
cd frontend && npm install && npm run dev
```

## Architecture

```
Browser (React) ──── POST /analyze ────► FastAPI Backend ──► Claude API
                                              │
                          Color-coded result ◄┘
                          (tactics + phrases + risk score)
```

## Example

Input:
```
Subject: URGENT: Your account will be suspended in 24 hours

Your PayPal account has been flagged. Act IMMEDIATELY to avoid permanent closure.
Click: http://paypa1-secure-login.account-verify.net/restore
```

Output:
```json
{
  "verdict": "PHISHING",
  "risk_score": 94,
  "tactics": [
    { "type": "URGENCY",       "phrase": "URGENT",              "severity": "HIGH" },
    { "type": "FEAR",          "phrase": "permanent closure",   "severity": "HIGH" },
    { "type": "IMPERSONATION", "phrase": "PayPal",              "severity": "HIGH" },
    { "type": "DECEPTION",     "phrase": "paypa1-secure-login", "severity": "HIGH" }
  ],
  "attacker_goal": "Click the malicious link to steal credentials"
}
```

## Use cases

- **Security awareness training** — show employees how phishing works
- **Email gateway enrichment** — flag suspicious emails automatically  
- **Incident response** — analyze messages during investigations
- **Research** — study social engineering patterns at scale
- **Personal protection** — verify suspicious messages before acting

## License

MIT
