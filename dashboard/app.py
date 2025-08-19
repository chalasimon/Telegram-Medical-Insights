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


# Example: Message Search
st.header("Search Messages")
search_term = st.text_input("Enter keyword to search messages:")
if search_term:
    try:
        query = f"SELECT id as message_id, channel_id, message FROM fct_messages WHERE message ILIKE '%{search_term}%' LIMIT 20;"
        df_search = pd.read_sql(query, conn)
        st.write(df_search)
    except Exception as e:
        st.warning(f"Could not search messages: {e}")

conn.close()