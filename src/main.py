from fastapi import FastAPI

app = FastAPI(
    title="Spidey AI",
    description="60-Day Roadmap - Day 4"
)


@app.get("/")
def root():
    return {
        "message": "Spidey is waking up!",
        "status": "active",
        "day": 4
    }


@app.get("/health")
def health_check():
    return {"status": "Database & Systems Normal"}


@app.get("/about")
def about():
    return {
        "name": "Spidey AI",
        "creator": "Kashan",
        "version": "0.1",
        "tech_stack": ["Python", "FastAPI", "OpenAI"],
        "mission": "Personal AI assistant"
    }