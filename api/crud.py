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
# get channel activity
def get_channel_activity(channel_name: str):
    query = """
        SELECT
            channel_name,
            COUNT(*) FILTER (WHERE date >= CURRENT_DATE - INTERVAL '1 day') AS daily_posts,
            COUNT(*) FILTER (WHERE date >= CURRENT_DATE - INTERVAL '7 days') AS weekly_posts
        FROM fct_messages
        WHERE channel_name = %s
        GROUP BY channel_name;
    """
    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, (channel_name,))
            result = cur.fetchone()
            return result
