#!/usr/bin/env python3
"""
Day 5 – Gemini CLI extractor (last automated run)
Reads OCR text, returns ONLY valid rule objects → JSONL
"""
import json, os, sys, subprocess, re
from pathlib import Path

txt_path   = Path(sys.argv[1])
prompt_txt = Path("prompts/extract_rules.txt").read_text()
ocr_text   = txt_path.read_text(encoding="utf-8")[:30000]

prompt = f"{prompt_txt}\n\n[START OCR TEXT]\n{ocr_text}\n[END OCR TEXT]"

proc = subprocess.run(
    ["gemini", "ask", "-p", prompt],
    text=True,
    capture_output=True,
)
if proc.returncode != 0 or not proc.stdout.strip():
    print("❌ Gemini error:", proc.stderr, file=sys.stderr)
    sys.exit(1)

raw = proc.stdout.strip()

# 1️⃣  grab the **first** JSON array with regex
match = re.search(r'\[[\s\S]*?\]', raw)
if not match:
    print("❌ No JSON array found", file=sys.stderr)
    sys.exit(1)

# 2️⃣  attempt to parse; if still broken → dump to file for manual fix
try:
    data = json.loads(match.group(0))
except json.JSONDecodeError as e:
    bad = Path("extracted") / f"{txt_path.stem}_raw.txt"
    bad.write_text(raw, encoding="utf-8")
    print(f"❌ Mal-formed JSON – saved raw to {bad} for manual repair")
    sys.exit(1)

REQUIRED = {"id", "original_text", "conditions", "effects", "metadata"}
os.makedirs("extracted", exist_ok=True)
out_file = f"extracted/{txt_path.stem}.jsonl"
valid = 0
with open(out_file, "w") as f:
    for obj in data:
        if (isinstance(obj, dict) and
            REQUIRED.issubset(obj) and
            isinstance(obj.get("metadata"), dict)):
            obj["metadata"].setdefault("source_name", txt_path.name)
            f.write(json.dumps(obj, ensure_ascii=False, separators=(",", ":")) + "\n")
            valid += 1

print(f"✅ {valid} rules → {out_file}")