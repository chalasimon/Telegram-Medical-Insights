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
st.text_input("Enter keyword to search products:", help="Type a product or keyword to filter messages.")
st.markdown("ℹ️ **Tip:** Use the filters below to refine your search results.", unsafe_allow_html=True)
date_range = st.date_input("Select date range:", [])
try:
    query = "SELECT message_id, channel_id, message, date FROM fct_messages WHERE TRUE"
    params = []
    if search_term:
        query += " AND message ILIKE %s"
        params.append(f"%{search_term}%")
    if len(date_range) == 2:
        query += " AND date BETWEEN %s AND %s"
        params.extend([date_range[0], date_range[1]])
    query += " LIMIT 50;"
    df_search = pd.read_sql(query, conn, params=params if params else None)
    st.write(df_search)
    # Time series visualization
    if 'date' in df_search.columns and not df_search.empty:
        df_search['date'] = pd.to_datetime(df_search['date'])
        st.line_chart(df_search.groupby(df_search['date'].dt.date).size(), use_container_width=True)
        st.caption("Hover over the chart for daily message counts.")
except Exception as e:
    st.warning(f"Could not search messages: {e}")

# Additional filters
min_length = st.slider("Minimum message length", min_value=0, max_value=500, value=0, help="Filter messages by minimum length.")
# Example: If you have product categories in your data
category_options = ["All"] + list(df_search['product_category'].unique()) if 'product_category' in df_search.columns else []
selected_category = st.selectbox("Product Category", options=category_options, help="Filter by product category.")

# Update query logic
if min_length > 0:
    query += " AND LENGTH(message) >= %s"
    params.append(min_length)
if selected_category and selected_category != "All":
    query += " AND product_category = %s"
    params.append(selected_category)

# Example: Top Products
st.header("Top Mentioned Products")
product_filter = st.text_input("Filter products:", help="Type to filter top products.")
try:
    query = "SELECT message as product_name, COUNT(*) as mention_count FROM fct_messages GROUP BY message ORDER BY mention_count DESC LIMIT 10;"
    df_products = pd.read_sql(query, conn)
    if product_filter:
        df_products = df_products[df_products['product_name'].str.contains(product_filter, case=False, na=False)]
    st.bar_chart(df_products.set_index("product_name"))
    st.subheader("Summary Panel")
    st.write(f"Total unique products: {df_products['product_name'].nunique()}")
    st.write(f"Most mentioned product: {df_products.loc[df_products['mention_count'].idxmax(), 'product_name']} ({df_products['mention_count'].max()} mentions)")
    st.write(df_products.describe())
except Exception as e:
    st.warning(f"Could not load top products: {e}")

# Example: Channel Activity
st.header("Channel Activity")
try:
    # Channel filter
    query_channels = "SELECT DISTINCT channel_id FROM fct_messages;"
    df_channel_list = pd.read_sql(query_channels, conn)
    channel_options = df_channel_list['channel_id'].tolist()
    selected_channel = st.selectbox("Select Channel", options=["All"] + channel_options, help="Choose a channel to filter activity.")
    date_range_channel = st.date_input("Select date range for channel activity:", [])
    if selected_channel == "All":
        query = "SELECT channel_id, COUNT(*) AS total_posts FROM fct_messages WHERE TRUE"
        params = []
        if len(date_range_channel) == 2:
            query += " AND date BETWEEN %s AND %s"
            params.extend([date_range_channel[0], date_range_channel[1]])
        query += " GROUP BY channel_id"
        df_channels = pd.read_sql(query, conn, params=params if params else None)
    else:
        query = "SELECT channel_id, COUNT(*) AS total_posts FROM fct_messages WHERE channel_id = %s"
        params = [selected_channel]
        if len(date_range_channel) == 2:
            query += " AND date BETWEEN %s AND %s"
            params.extend([date_range_channel[0], date_range_channel[1]])
        query += " GROUP BY channel_id"
        df_channels = pd.read_sql(query, conn, params=params)
    st.dataframe(df_channels)
    # Business insights panel
    st.subheader("Business Insights")
    if not df_channels.empty:
        st.write(f"Channel with most posts: {df_channels.loc[df_channels['total_posts'].idxmax(), 'channel_id']} ({df_channels['total_posts'].max()} posts)")
        st.write(f"Total messages in selected range: {df_channels['total_posts'].sum()}")
        # Trend visualization
        if len(date_range_channel) == 2:
            query_trend = "SELECT date::date, COUNT(*) as posts FROM fct_messages WHERE date BETWEEN %s AND %s GROUP BY date::date ORDER BY date::date"
            df_trend = pd.read_sql(query_trend, conn, params=[date_range_channel[0], date_range_channel[1]])
            st.line_chart(df_trend.set_index('date')['posts'])
except Exception as e:
    st.warning(f"Could not load channel activity: {e}")


conn.close()