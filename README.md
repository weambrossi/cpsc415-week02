# Week 2: Chat client

Ethan Ambrossi · CPSC 415

`chat.py` sends one question to a model through OpenRouter. It prints the answer, starting with "Sir,", and then a line with the model name and the input and output token counts. It uses only the Python standard library.

## How to run it

```bash
export CHAT_BASE_URL=https://openrouter.ai/api/v1
export CHAT_MODEL=qwen/qwen3.8-27b:free
export OPENROUTER_API_KEY=...   # your key; never commit it
python3 chat.py "In one sentence, what is a context window?"
```

Example output:

```
Sir, A context window is the maximum amount of text an AI model can process at one time.

model: qwen/qwen3.8-27b:free | input tokens: 67 | output tokens: 1448
```

To use a different model, change only `CHAT_MODEL`.

**If you get `CERTIFICATE_VERIFY_FAILED` on macOS:** the python.org installer doesn't set up certificates. Either run `/Applications/Python 3.13/Install Certificates.command` once, or point Python at the macOS system bundle with `export SSL_CERT_FILE=/etc/ssl/cert.pem`. The runs in `CHECKS.md` used the second option.

## Changes to the intent draft

1. **It calls me "sir."** The draft had nothing like this. I want every answer to start with "sir," so I added it as a success criterion. The program adds "Sir, " in code rather than asking the model in the system prompt, so it happens every time even if the model ignores instructions.
2. **OpenRouter only, no local model.** The draft left open whether I'd try Ollama and which key variable the program should read. I removed that question and put local models under "Not in scope." Everything goes through OpenRouter and reads `OPENROUTER_API_KEY`.

After approval, the build changed `max_tokens` from 1000 to 4000. At 1000, Qwen used all 1000 tokens on hidden reasoning and returned an empty answer. The intent records this change and why.

## One line of the code

```python
usage = data.get("usage", {})
```

`chat.py:72`: `data` is the parsed JSON response from `/chat/completions`. The `usage` object is where the provider reports what the call cost in tokens: `prompt_tokens` is what I sent (system message plus question), and `completion_tokens` is what the model generated, including hidden reasoning. The last line prints these two numbers, and they are what I compared against OpenRouter's record. `.get(..., {})` means that if a provider leaves out `usage`, the program prints `None` instead of crashing.

## Two models, one question

| Model | Answer | Tokens (in / out) | Observed cost |
|---|---|---|---|
| `qwen/qwen3.8-27b:free` | "A context window is the maximum amount of text an AI model can process at one time." | 67 / 1448 (1429 reasoning) | $0 (free model) |
| `nvidia/nemotron-3-super-120b-a12b:free` | "A context window is the fixed-size span of tokens (such as words or subword units) that a language model can simultaneously attend to when processing or generating text." | 30 / 82 (54 reasoning) | $0 (free model) |

Qwen gave a plain-language answer, and Nemotron gave a more technical one that talks about tokens. On this one question, Qwen spent far more tokens reasoning before it answered. Both costs were $0 because both are free models. Costs and token counts come from OpenRouter's record of each request (see `CHECKS.md`). This compares one question and is not a benchmark.

## Local model

Not tried. Local models are out of scope in the intent.

## Future goal: multi-turn chat

I want this to keep a conversation going eventually. That is out of scope for Week 2 and will be a spec question in Week 3. The program would have to keep a list of messages and resend the whole list each turn, so input tokens (and cost) grow with every question.
