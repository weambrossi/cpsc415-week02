# Intent: chat client

## Goal
A command-line program that takes a question, sends it to an AI model through OpenRouter, and prints the model's answer, the model's name, and the token counts.

## Who it is for
Me, a student learning how to use the OpenRouter API. Later, a quick way to ask questions from the terminal without opening a browser.

## Constraints
- Python 3, standard library only (no packages, no pip install).
- One question per run, passed on the command line; one answer printed.
- Configuration comes from environment variables: `CHAT_BASE_URL` (API address), `CHAT_MODEL` (model ID), and `OPENROUTER_API_KEY` (key). Nothing secret in the code or the repository.
- Changing only `CHAT_MODEL` must point it at a different model with no code change.
- Model: `qwen/qwen3.8-27b:free` (free tier, so subject to OpenRouter rate limits).
- `max_tokens` = 1000, leaving room for hidden reasoning tokens plus the visible answer.
- Default system prompt: "concise as possible".

## Not in scope
- Streaming responses.
- Chat history or multi-turn conversation (a future goal; see Open questions).
- A web page or GUI.
- Retries.
- More than one provider at a time.
- Local models (Ollama). Everything goes through OpenRouter.

## Success looks like
1. It answers a question through OpenRouter.
2. The model name and token counts it prints match OpenRouter's Activity page.
3. Every answer is followed by the model used and the token usage (input and output tokens).
4. Every answer starts by calling me "sir".

## Open questions
- Error handling: when the key is missing, the model ID is wrong, or the request fails, should it print a short message and exit, or show the raw error?
- Future goal: multi-turn chat with history. To be specified in Week 3, not built now.

**Approved by:** Ethan Ambrossi, 2026-09-22
