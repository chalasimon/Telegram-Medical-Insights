import streamlit as st
import pandas as pd
import psycopg2

st.title("Telegram Medical Insights Dashboard")

# Database connection
conn = psycopg2.connect(
    host="localhost",
    dbname="your_db_name",
    user="your_db_user",
    password="your_db_password",
    port=5432
)

# Example: Top Products
st.header("Top Mentioned Products")
query = "SELECT product_name, mention_count FROM top_products ORDER BY mention_count DESC LIMIT 10;"
df_products = pd.read_sql(query, conn)
st.bar_chart(df_products.set_index("product_name"))

# Example: Channel Activity
st.header("Channel Activity")
query = "SELECT channel_id, daily_posts, weekly_posts FROM channel_activity;"
df_channels = pd.read_sql(query, conn)
st.dataframe(df_channels)

# Example: Message Search
st.header("Search Messages")
search_term = st.text_input("Enter keyword to search messages:")
if search_term:
    query = f"SELECT message_id, channel_id, message FROM messages WHERE message ILIKE '%{search_term}%' LIMIT 20;"
    df_search = pd.read_sql(query, conn)
    st.write(df_search)

conn.close()