from fastapi import FastAPI
import uvicorn

app = FastAPI(
    title="Spidey AI",
    description="60-Day Roadmap - Day 2"
)

@app.get("/")
def root():
    return {
        "message": "Spidey is waking up!", 
        "status": "active",
        "day": 2
    }

@app.get("/health")
def health_check():
    return {"status": "Database & Systems Normal"}