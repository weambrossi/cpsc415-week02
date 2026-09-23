"""Send one question to a chat model and print the answer, model, and token usage.

Usage:
    python3 chat.py "your question"

Environment:
    CHAT_BASE_URL       API address, e.g. https://openrouter.ai/api/v1
    CHAT_MODEL          model ID, e.g. qwen/qwen3.8-27b:free
    OPENROUTER_API_KEY  your OpenRouter key (never put it in this file)
"""

import json
import os
import sys
import urllib.error
import urllib.request

SYSTEM_PROMPT = "concise as possible"
MAX_TOKENS = 4000


def fail(message):
    print(f"Error: {message}", file=sys.stderr)
    sys.exit(1)


def main():
    if len(sys.argv) != 2:
        fail('usage: python3 chat.py "your question"')
    question = sys.argv[1]

    base_url = os.environ.get("CHAT_BASE_URL")
    model = os.environ.get("CHAT_MODEL")
    api_key = os.environ.get("OPENROUTER_API_KEY")
    for name, value in [("CHAT_BASE_URL", base_url), ("CHAT_MODEL", model),
                        ("OPENROUTER_API_KEY", api_key)]:
        if not value:
            fail(f"{name} is not set")

    # The request: a model, a system message, a user message, and a length cap.
    body = {
        "model": model,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": question},
        ],
        "max_tokens": MAX_TOKENS,
    }
    request = urllib.request.Request(
        base_url.rstrip("/") + "/chat/completions",
        data=json.dumps(body).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=120) as response:
            data = json.load(response)
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", errors="replace")
        fail(f"HTTP {e.code} from {base_url}: {detail}")
    except urllib.error.URLError as e:
        fail(f"could not reach {base_url}: {e.reason}")

    if "error" in data:
        fail(data["error"].get("message", str(data["error"])))

    answer = (data["choices"][0]["message"].get("content") or "").strip()
    usage = data.get("usage", {})

    print(f"Sir, {answer}")
    print()
    print(f"model: {data.get('model', model)} | "
          f"input tokens: {usage.get('prompt_tokens')} | "
          f"output tokens: {usage.get('completion_tokens')}")


if __name__ == "__main__":
    main()
