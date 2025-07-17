#!/usr/bin/env python3
import duckdb
import json
from pathlib import Path

# Path to the JSONL file
JSONL_PATH = Path('data/extracted/samplepdf1-20.jsonl')
DB_PATH = 'vedic_ai.duckdb'

# Connect to DuckDB
conn = duckdb.connect(DB_PATH)

# Create table (adjusted for available fields)
conn.execute("""
CREATE TABLE IF NOT EXISTS rules (
    id VARCHAR PRIMARY KEY,
    original_text VARCHAR,
    conditions JSON,
    effects JSON,
    metadata JSON,
    source_name VARCHAR,
    confidence VARCHAR
)
""")

# Load data from JSONL file
with open(JSONL_PATH, 'r', encoding='utf-8') as f:
    for line in f:
        rule = json.loads(line)
        metadata = rule.get('metadata', {})
        conn.execute(
            "INSERT OR REPLACE INTO rules VALUES (?, ?, ?, ?, ?, ?, ?)",
            [
                rule.get('id'),
                rule.get('original_text'),
                json.dumps(rule.get('conditions', {}), ensure_ascii=False),
                json.dumps(rule.get('effects', []), ensure_ascii=False),
                json.dumps(metadata, ensure_ascii=False),
                metadata.get('source_name', ''),
                metadata.get('confidence', '')
            ]
        )

# Verification step: print row count
row_count = conn.execute('SELECT COUNT(*) FROM rules').fetchone()[0]
print(f"Data loaded into DuckDB successfully. Row count: {row_count}")