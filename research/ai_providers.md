# Spidey — AI Providers Research

## Available AI Providers

| Provider | Best Model | Free? | Speed | Best For |
|----------|-----------|-------|-------|----------|
| OpenAI | GPT-4o-mini | Paid (cheap) | Fast | General tasks & coding |
| Anthropic | Claude Haiku/Sonnet | Paid | Fast | Code review & analysis |
| Google | Gemini Flash | ✅ Free tier | Fast | Research & multimodal |
| DeepSeek | DeepSeek V3 | Very cheap | Medium | Python coding |
| Ollama | Llama/Qwen (local) | ✅ Free | Local | Offline fallback |

---

## For Development (Our Coding Help):
1. **Claude** — Best for code review & clean architecture
2. **ChatGPT** — Best for debugging & system design
3. **DeepSeek** — Best for Python functions (cheapest option)
4. **Gemini** — Best for research & comparing libraries

## For Spidey's Brain (Runtime — when app runs):
- **Primary:** OpenAI GPT-4o-mini (fast, cheap, reliable)
- **Secondary:** Claude Haiku (backup provider)
- **Free:** Gemini Flash (Google free tier, rate limited)
- **Offline:** Ollama + Llama 3.2 (no internet needed)

## API Pricing (approximate per 1M tokens):
- GPT-4o-mini: ~$0.15 input / ~$0.60 output
- Claude Haiku: ~$0.25 input / ~$1.25 output
- DeepSeek V3: ~$0.14 input / ~$0.28 output
- Gemini Flash: FREE (with rate limits)
- Ollama: FREE (runs locally on your PC)

---
