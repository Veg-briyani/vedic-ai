#!/usr/bin/env python3
import duckdb

# Connect to DuckDB
db_path = 'vedic_ai.duckdb'
conn = duckdb.connect(db_path)

# Index creation statements
indexes = [
    "CREATE INDEX IF NOT EXISTS idx_rules_id ON rules(id);",
    "CREATE INDEX IF NOT EXISTS idx_rules_original_text ON rules(original_text);",
    "CREATE INDEX IF NOT EXISTS idx_rules_source_name ON rules(source_name);",
    "CREATE INDEX IF NOT EXISTS idx_rules_confidence ON rules(confidence);"
]

for stmt in indexes:
    conn.execute(stmt)

print("Indexes created successfully.") 