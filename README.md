# Spidey AI Assistant

**Author:** Rana Kashan (spidy10-max)

## Description
Spidey AI Assistant is a personal AI assistant that provides voice interaction, memory, and computer control capabilities to help automate tasks, answer questions, and assist the user in daily workflows.

## Planned Features
- Voice input (microphone) and speech output
- Long-term memory and short-term context
- Local file and app control (automation)
- Web search and external API integration
- Task scheduling and reminders
- Secure settings and user preferences

## Tech Stack
- Python
- FastAPI
- SQLite
- ChromaDB
- Whisper (speech-to-text)
- Piper (TTS)
- PyAutoGUI (desktop automation)

## Setup Instructions
1. Create a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Run the development server (FastAPI + Uvicorn):

```powershell
uvicorn src.main:app --reload --host 127.0.0.1 --port 8000
```

4. Configure environment variables by adding a `.env` file at the project root.

## Author
Rana Kashan (spidy10-max)
