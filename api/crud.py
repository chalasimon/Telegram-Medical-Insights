
from psycopg2.extras import RealDictCursor
from .database import get_db_connection

def get_top_products(limit: int = 10):
    """
    Returns the top mentioned products/messages.
    This assumes 'message' contains product mentions. Adjust as needed for your schema.
    """
    query = """
        SELECT message AS product_name, COUNT(*) as mention_count
        FROM fct_messages
        WHERE message IS NOT NULL
        GROUP BY message
        ORDER BY mention_count DESC
        LIMIT %s;
    """
    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, (limit,))
            return cur.fetchall()

def get_channel_activity(channel_id: str):
    """
    Returns daily and weekly post counts for a given channel_id (rolling window).
    """
    query = """
        SELECT
            channel_id,
            COUNT(*) FILTER (WHERE date >= CURRENT_DATE - INTERVAL '1 day') AS daily_posts,
            COUNT(*) FILTER (WHERE date >= CURRENT_DATE - INTERVAL '7 days') AS weekly_posts
        FROM fct_messages
        WHERE channel_id = %s
        GROUP BY channel_id;
    """
    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, (channel_id,))
            result = cur.fetchone()
            return result

def search_messages(query_str: str):
    """
    Searches messages containing the query string.
    """
    query = """
        SELECT message_id, channel_id, message
        FROM fct_messages
        WHERE message ILIKE %s
        LIMIT 50;
    """
    with get_db_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, (f"%{query_str}%",))
            return cur.fetchall()