# ai-devops-incident-copilot
A DevOps capstone with CI/CD, infrastructure as code, monitoring, security scanning, and an AI incident assistant.

## About
AI DevOps Incident Copilot helps investigate and summarize DevOps incidents.

## First feature: incident analysis

The API includes a deterministic first-pass analyzer for common log patterns such as out-of-memory kills, container crash loops, upstream connection failures, and request timeouts. It returns a summary, severity, likely cause, confidence, matching evidence, and read-only investigation steps. It does not execute commands or change infrastructure.

### Run locally

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open `http://127.0.0.1:8000/docs` to try the API interactively.

### Analyze an incident

Send a `POST` request to `/api/incidents/analyze` with JSON like:

```json
{
  "title": "Checkout API returns 502",
  "description": "Requests started failing after the latest deployment.",
  "logs": "upstream connection refused"
}
```

The response includes the likely cause, severity, confidence, matching log evidence, and suggested read-only checks. If no known pattern matches, the analyzer says the evidence is insufficient instead of guessing.


## Run with Docker Compose

Make sure Docker Desktop is open, then run:

```powershell
docker compose up --build
## Gemini AI setup

Copy `.env.example` to `.env` with `Copy-Item .env.example .env`, then open it with `notepad .env` and replace the key placeholder. Keep `.env` private; it is ignored by Git.

Run `docker compose up --build` and open `http://127.0.0.1:8001/docs`. With a Gemini key, incident text is sent to Google for analysis; use synthetic demo logs. Without a key, the app uses its rule-based fallback.
