from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
import duckdb
from typing import Optional

app = FastAPI()

# Enable CORS for all origins (for development)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Connect to DuckDB
db_path = 'vedic_ai.duckdb'
conn = duckdb.connect(db_path)

@app.get("/rules")
async def get_rules(
    id: Optional[str] = Query(None),
    source_name: Optional[str] = Query(None),
    confidence: Optional[float] = Query(None)
):
    query = "SELECT * FROM rules"
    params = []
    where_clauses = []

    if id:
        where_clauses.append("id = ?")
        params.append(id)
    if source_name:
        where_clauses.append("source_name = ?")
        params.append(source_name)
    if confidence is not None:
        where_clauses.append("CAST(confidence AS DOUBLE) > ?")
        params.append(confidence)

    if where_clauses:
        query += " WHERE " + " AND ".join(where_clauses)

    cursor = conn.cursor()
    cursor.execute(query, params)
    rules = cursor.fetchall()
    columns = [desc[0] for desc in cursor.description]

    if not rules:
        raise HTTPException(status_code=404, detail="No rules found")

    # Return as list of dicts for better JSON output
    result = [dict(zip(columns, row)) for row in rules]
    return {"rules": result} 