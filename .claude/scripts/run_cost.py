"""Work out what the website-tester agents of one run cost, in US dollars, and save it in RUN/run_timing.json.

Usage:
    python3 run_cost.py <RUN> [--projects-dir DIR]

Claude Code saves each agent's transcript as
    ~/.claude/projects/<project>/<session>/subagents/agent-<id>.jsonl
This script finds the transcripts whose first prompt names the RUN folder (every batch prompt from
/run-tests does), reads the usage of every API response once (deduplicated by message id) and prices
it per model. The result is written to run_timing.json as "cost":

    {"total_usd": 3.90, "by_type_usd": {"input": .., "output": .., "cache_write": .., "cache_read": ..},
     "tokens": {"input": .., "output": .., "cache_write": .., "cache_read": ..},
     "api_calls": 133, "models": ["claude-sonnet-5-5"], "batches_found": 4, "estimated": false,
     "prices": "...", "note": "..."}

Only the website-tester agents are counted. The coordinator session also does other work, so it is
not included. Prices are API list prices (per million tokens), not what our plan bills.
"""
import json
import sys
from pathlib import Path

# Per million tokens. cache_write_5m / cache_write_1h / cache_read are given where the pricing reference
# lists them; otherwise they use the standard ratios (1.25x, 2x, 0.1x input) and the cost is marked estimated.
PRICES = {
    "claude-opus-5-5": {"input": 4.00, "output": 20.00, "cache_write_5m": 5.00, "cache_write_1h": 8.00,
                        "cache_read": 0.20},
    "claude-sonnet-5-5": {"input": 2.00, "output": 10.00, "cache_write_5m": 2.50, "cache_write_1h": 4.00,
                          "cache_read": 0.20},
    # Haiku 5.5: $0.10 / $0.50 for prompts up to 100K tokens, $0.50 / $2.50 above. Cache prices estimated.
    "claude-haiku-5-5": {"input": 0.10, "output": 0.50, "long_input": 0.50, "long_output": 2.50,
                         "long_threshold": 100_000, "estimated_cache": True},
}
PRICES_NOTE = "API list prices per million tokens; Opus 5.5 $4/$20, Sonnet 5.5 $2/$10, Haiku 5.5 $0.10/$0.50"


def price_for(model):
    for key, p in PRICES.items():
        if model and model.startswith(key):
            return key, p
    return None, None


def first_prompt(path):
    with open(path, encoding="utf-8", errors="ignore") as f:
        for line in f:
            try:
                d = json.loads(line)
            except ValueError:
                continue
            if d.get("type") == "user":
                c = d.get("message", {}).get("content")
                if isinstance(c, str):
                    return c
                if isinstance(c, list):
                    return " ".join(x.get("text", "") for x in c if isinstance(x, dict))
    return ""


def usages(path):
    seen = {}
    with open(path, encoding="utf-8", errors="ignore") as f:
        for line in f:
            try:
                d = json.loads(line)
            except ValueError:
                continue
            m = d.get("message") or {}
            if d.get("type") == "assistant" and isinstance(m, dict) and m.get("usage") and m.get("id"):
                seen[m["id"]] = (m.get("model"), m["usage"])
    return list(seen.values())


def cost_of(model, u):
    key, p = price_for(model)
    if not p:
        return None
    cc = u.get("cache_creation") or {}
    c5, c1 = cc.get("ephemeral_5m_input_tokens"), cc.get("ephemeral_1h_input_tokens")
    if c5 is None and c1 is None:
        c5, c1 = u.get("cache_creation_input_tokens", 0), 0
    c5, c1 = c5 or 0, c1 or 0
    inp, out, cr = u.get("input_tokens", 0), u.get("output_tokens", 0), u.get("cache_read_input_tokens", 0)
    pin, pout = p["input"], p["output"]
    if "long_threshold" in p and inp + cr + c5 + c1 > p["long_threshold"]:
        pin, pout = p["long_input"], p["long_output"]
    w5, w1, r = p.get("cache_write_5m", pin * 1.25), p.get("cache_write_1h", pin * 2), p.get("cache_read", pin * 0.1)
    if "long_threshold" in p:
        w5, w1, r = pin * 1.25, pin * 2, pin * 0.1
    tokens = {"input": inp, "output": out, "cache_write": c5 + c1, "cache_read": cr}
    usd = {"input": inp * pin / 1e6, "output": out * pout / 1e6, "cache_write": (c5 * w5 + c1 * w1) / 1e6,
           "cache_read": cr * r / 1e6}
    return key, tokens, usd, bool(p.get("estimated_cache"))


def main(argv):
    if not argv:
        print(__doc__)
        return 2
    run = Path(argv[0]).resolve()
    projects = Path.home() / ".claude" / "projects"
    if "--projects-dir" in argv:
        projects = Path(argv[argv.index("--projects-dir") + 1])
    timing_file = run / "run_timing.json"
    if not timing_file.exists():
        print(f"No run_timing.json in {run}")
        return 2
    # macOS paths are case-insensitive (".../Github/..." and ".../GitHub/..." are the same folder),
    # so match the run path without case.
    marker = str(run).lower()
    files = [f for f in projects.glob("*/*/subagents/*.jsonl") if marker in first_prompt(f).lower()]
    if not files:
        print(f"No website-tester transcripts found that name {run}. Cost not added.")
        return 1

    tokens = {"input": 0, "output": 0, "cache_write": 0, "cache_read": 0}
    usd = {k: 0.0 for k in tokens}
    models, calls, estimated, unknown = set(), 0, False, set()
    for f in files:
        for model, u in usages(f):
            r = cost_of(model, u)
            if r is None:
                unknown.add(model)
                continue
            key, t, c, est = r
            models.add(key)
            calls += 1
            estimated = estimated or est
            for k in tokens:
                tokens[k] += t[k]
                usd[k] += c[k]
    cost = {
        "total_usd": round(sum(usd.values()), 2),
        "by_type_usd": {k: round(v, 2) for k, v in usd.items()},
        "tokens": tokens,
        "api_calls": calls,
        "models": sorted(models),
        "batches_found": len(files),
        "estimated": estimated,
        "prices": PRICES_NOTE,
        "note": "website-tester agents only; the coordinator is not included"
                + ("; Haiku cache prices estimated (0.1x read, 1.25x write)" if estimated else "")
                + (f"; no price for {sorted(m for m in unknown if m)}" if unknown else ""),
    }
    timing = json.loads(timing_file.read_text())
    timing["cost"] = cost
    timing_file.write_text(json.dumps(timing, indent=1) + "\n")
    print(f"{run.name}: ${cost['total_usd']} ({', '.join(cost['models'])}, {calls} API calls, "
          f"{len(files)} transcripts{', estimated' if estimated else ''})")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
