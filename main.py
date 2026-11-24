from typing import Literal

from fastapi import FastAPI
from pydantic import BaseModel, Field

app = FastAPI(title="AI DevOps Incident Copilot")


class IncidentRequest(BaseModel):
    title: str = Field(min_length=3, max_length=200)
    description: str = Field(min_length=3, max_length=4000)
    logs: str = Field(default="", max_length=20000)


class IncidentAnalysis(BaseModel):
    summary: str
    severity: Literal["low", "medium", "high", "critical"]
    likely_cause: str
    confidence: float
    evidence: list[str]
    recommended_steps: list[str]


def analyze_incident(incident: IncidentRequest) -> IncidentAnalysis:
    """Provide a deterministic first-pass diagnosis from common log patterns."""
    text = f"{incident.title}\n{incident.description}\n{incident.logs}".lower()

    if "oomkilled" in text or "out of memory" in text or "oom kill" in text:
        cause = "The service may have exceeded its memory limit."
        evidence = [term for term in ("oomkilled", "out of memory", "oom kill") if term in text]
        severity = "high"
        confidence = 0.82
        steps = [
            "Check recent memory usage and restart counts for the affected service.",
            "Compare memory limits and traffic levels with the last healthy period.",
            "Review recent deployments for memory-intensive changes.",
        ]
    elif "crashloopbackoff" in text or "crash loop" in text:
        cause = "The container is repeatedly starting and exiting."
        evidence = [term for term in ("crashloopbackoff", "crash loop") if term in text]
        severity = "high"
        confidence = 0.8
        steps = [
            "Inspect the previous container's startup logs and exit code.",
            "Check whether required environment variables and dependencies are available.",
            "Compare the failing container image with the last healthy deployment.",
        ]
    elif "502" in text or "connection refused" in text or "upstream unavailable" in text:
        cause = "The proxy or caller cannot connect to the upstream service."
        evidence = [term for term in ("502", "connection refused", "upstream unavailable") if term in text]
        severity = "high"
        confidence = 0.78
        steps = [
            "Check the upstream service health and whether it is listening on the expected port.",
            "Verify service discovery, target addresses, and recent network changes.",
            "Review proxy error logs and the upstream service logs for matching timestamps.",
        ]
    elif "timeout" in text or "timed out" in text or "504" in text:
        cause = "A request to a dependent service may be taking too long or timing out."
        evidence = [term for term in ("timeout", "timed out", "504") if term in text]
        severity = "medium"
        confidence = 0.68
        steps = [
            "Compare request latency and error rates across the affected service and its dependencies.",
            "Check for resource saturation or slow database queries around the incident time.",
            "Review recent deployments and configuration changes for timeout or retry settings.",
        ]
    else:
        cause = "There is not enough recognized evidence to identify a likely cause."
        evidence = []
        severity = "medium"
        confidence = 0.25
        steps = [
            "Collect the exact incident time, affected service, and a short log window around the failure.",
            "Check service health, recent deployments, and resource usage for the same time window.",
            "Add relevant error messages or alert details and analyze the incident again.",
        ]

    summary = f"{incident.title.strip()}: {cause}"
    return IncidentAnalysis(
        summary=summary,
        severity=severity,
        likely_cause=cause,
        confidence=confidence,
        evidence=evidence,
        recommended_steps=steps,
    )


@app.get("/")
def home():
    return {"message": "Incident Copilot is running"}


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/api/incidents/analyze", response_model=IncidentAnalysis)
def analyze(incident: IncidentRequest) -> IncidentAnalysis:
    return analyze_incident(incident)
