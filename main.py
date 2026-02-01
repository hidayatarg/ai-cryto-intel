from fastapi import FastAPI

app = FastAPI(title="AI Crypto Market Intelligence")

@app.get("/health")
def health():
    return {"status": "ok"}