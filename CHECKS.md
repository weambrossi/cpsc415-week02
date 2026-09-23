# Checks

Question for every run: "In one sentence, what is a context window?" All runs were on 2026-09-22 with `CHAT_BASE_URL=https://openrouter.ai/api/v1`.

The "provider record" is OpenRouter's own record of each request, looked up by generation ID with `GET /api/v1/generation?id=...`. This is the same data the Activity page shows, and it doesn't come from the program's output.

| Check | Expected | Observed | Pass/fail |
|---|---|---|---|
| Question through OpenRouter | An answer and a usage line | `Sir, A context window is the maximum amount of text an AI model can process at one time.` and then `model: qwen/qwen3.8-27b:free \| input tokens: 67 \| output tokens: 1448` | Pass |
| Usage record matches | Same model; same or close token counts | Provider record `gen-1790121651-DQeVWtUWttkn7VsCHtW1`: model `qwen/qwen3.8-27b-20260814:free` (the dated version of the same model), native tokens 67 in / 1448 out, which match exactly. 1429 of the 1448 output tokens were reasoning. OpenRouter's normalized counts are different (17 / 1438); the program prints the native counts. | Pass |
| System prompt changed | Answer style changes accordingly | Changed the system prompt from "concise as possible" to "Answer like a pirate.": `Sir, A context window be the ship's memory, holdin' all the words and bits of info a AI can see at once before its riggin' gets overloaded, arr!` Tokens: 68 in / 118 out (82 reasoning). | Pass |
| `max_tokens` = 20 | Truncated or empty answer; tokens still billed | Empty answer (`Sir, ` followed by nothing). Output tokens: 20, and the record shows all 20 were reasoning, with `finish_reason: length`. Cost was $0 because the model is free, but the 20 tokens were still counted. | Pass |
| Model swapped (step 4) | Different model name in usage; answer may differ | Changed only `CHAT_MODEL` to `nvidia/nemotron-3-super-120b-a12b:free`: `Sir, A context window is the fixed-size span of tokens (such as words or subword units) that a language model can simultaneously attend to when processing or generating text.` Program: 30 in / 82 out. Record `gen-1790122067-djucTl4SFOxnWwwB1rNM`: 30 / 82 native, provider Nvidia. | Pass |
| Local model (optional) | Answer from localhost; no OpenRouter entry | Not attempted. Local models are out of scope in the intent; everything goes through OpenRouter. | N/A |

## Other things observed

- **The first run with `max_tokens` = 1000 returned an empty answer.** The record (`gen-1790121577-ON3vofKsh4RCIQdEGqrY`) shows all 1000 output tokens were reasoning, with `finish_reason: length`. The cap was raised to 4000, and the intent was amended to match.
- **Free models are often rate-limited.** Many attempts returned HTTP 429 ("temporarily rate-limited upstream"). The second model named in the plan, `google/gemma-4-31b-it:free`, never got through, so the swap used Nemotron instead.
- **Some errors come back with HTTP 200.** Nemotron once returned "Service temporarily overloaded" with a successful status code. The program checks the JSON body for an `error` field and prints it.
