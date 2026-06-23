# AI API Concepts — Day 8

## How AI APIs Work:
1. You send a POST request with messages
2. AI processes and returns a response
3. You display the response

## 3 Roles:
- **system**: Tells AI who it is (personality/rules)
- **user**: Human's message
- **assistant**: AI's response

## Key Parameters:
- **model**: Which AI model to use
- **temperature**: Creativity (0.0 = focused, 1.0 = balanced, 2.0 = random)
- **max_tokens**: Maximum response length
- **messages**: List of conversation messages

## API Providers We'll Use:
- **Groq** (FREE) — Llama 3.1 model — Super fast
- **OpenAI** (Paid) — GPT-4o — Most popular
- **Anthropic** (Paid) — Claude — Best for code
- **DeepSeek** (Cheap) — DeepSeek V3 — Good coder

## Important:
- All providers use similar message format
- Groq uses OpenAI-compatible API
- Same code works with multiple providers!