from fastapi import FastAPI

app = FastAPI(title="AI DevOps Incident Copilot")


@app.get("/")
def home():
    return {"message": "Incident Copilot is running"}


@app.get("/health")
def health():
    return {"status": "healthy"}
