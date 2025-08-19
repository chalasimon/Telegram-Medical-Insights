import os
from psycopg2.extras import RealDictCursor
from database import get_db_connection
def get_top_products(limit: int = 10):
    query = """
        SELECT product_name, COUNT(*) AS mention_count
        FROM fct_messages
        GROUP BY product_name
        ORDER BY mention_count DESC
        LIMIT %s;
    """
    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, (limit,))
            return cur.fetchall()
