import streamlit as st
import pandas as pd
import psycopg2
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.database.Connection import Database

st.title("Telegram Medical Insights Dashboard")

# Database connection
host = "localhost"
port = 5432
# get the database credentials from environment variables or use defaults
# you can set these in a .env file or directly in your environment
# for example, using dotenv package to load from .env file
from dotenv import load_dotenv
load_dotenv()

host=os.getenv("POSTGRES_HOST")
dbname=os.getenv("POSTGRES_DB")
user=os.getenv("POSTGRES_USER")
password=os.getenv("POSTGRES_PASSWORD")
port=os.getenv("POSTGRES_PORT")

# create a database connection
db = Database(host=host,database=dbname, user=user, password=password, port=port)
# connect to the database
conn = db.connect()


# Example: Product Search
st.header("Search Products")
search_term = st.text_input("Enter keyword to search products:")
if search_term:
    try:
        query = """
            SELECT message_id, channel_id, message, date
            FROM fct_messages
            WHERE message ILIKE %s
            LIMIT 50;
        """
        df_search = pd.read_sql(query, conn, params=(f"%{search_term}%",))
        st.write(df_search)
        # Time series visualization
        if 'date' in df_search.columns:
            df_search['date'] = pd.to_datetime(df_search['date'])
            st.line_chart(df_search.groupby(df_search['date'].dt.date).size())
    except Exception as e:
        st.warning(f"Could not search messages: {e}")

# Example: Top Products
st.header("Top Mentioned Products")
try:
    query = "SELECT message as product_name, COUNT(*) as mention_count FROM fct_messages GROUP BY message ORDER BY mention_count DESC LIMIT 10;"
    df_products = pd.read_sql(query, conn)
    st.bar_chart(df_products.set_index("product_name"))
except Exception as e:
    st.warning(f"Could not load top products: {e}")

# Example: Channel Activity
st.header("Channel Activity")
try:
    query = """
        SELECT channel_id,
               COUNT(*) FILTER (WHERE date >= CURRENT_DATE - INTERVAL '1 day') AS daily_posts,
               COUNT(*) FILTER (WHERE date >= CURRENT_DATE - INTERVAL '7 days') AS weekly_posts
        FROM fct_messages
        GROUP BY channel_id
    """
    df_channels = pd.read_sql(query, conn)
    st.dataframe(df_channels)
except Exception as e:
    st.warning(f"Could not load channel activity: {e}")




conn.close()