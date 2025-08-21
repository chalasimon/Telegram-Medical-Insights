import streamlit as st
import pandas as pd
import psycopg2
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.database.Connection import Database


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



# Using "with" notation
with st.sidebar:
    st.markdown("""
        <style>
        .sidebar-title {font-size:2em; font-weight:bold; color:#2c3e50; margin-bottom:0.5em;}
        .sidebar-nav .active {background-color:#e1eafc; color:#1a73e8; font-weight:bold; border-radius:8px;}
        .sidebar-nav button {width:100%; text-align:left; margin-bottom:0.5em; font-size:1.1em;}
        </style>
    """, unsafe_allow_html=True)
    st.markdown('<div class="sidebar-title">🩺 Dashboard</div>', unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("## Navigation")
    nav_options = [
        ("Search Products", "🔍 Search Products"),
        ("Top Mentioned Products", "🏆 Top Mentioned Products"),
        ("Channel Activity", "📊 Channel Activity")
    ]
    if "sidebar_task" not in st.session_state:
        st.session_state["sidebar_task"] = nav_options[0][0]
    for option, label in nav_options:
        if st.session_state["sidebar_task"] == option:
            btn_style = "sidebar-nav active"
        else:
            btn_style = "sidebar-nav"
        if st.button(label, key=option):
            st.session_state["sidebar_task"] = option
    task = st.session_state["sidebar_task"]
   




# Professional dashboard layout
st.markdown("""
    <style>
    .main-title {font-size:2.5em; font-weight:bold; color:#1a73e8; margin-bottom:0.2em;}
    .main-section {background-color:#f8fafc; border-radius:12px; padding:2em 2em 1em 2em; margin-bottom:2em; box-shadow:0 2px 8px #e1eafc;}
    .section-header {font-size:1.5em; font-weight:bold; color:#2c3e50; margin-bottom:1em;}
    </style>
""", unsafe_allow_html=True)
st.markdown('<div class="main-title">Telegram Medical Insights Dashboard</div>', unsafe_allow_html=True)

if task == "Search Products":

    st.markdown('<div class="section-header">🔍 Search Products</div>', unsafe_allow_html=True)
    search_term = st.text_input("Enter keyword to search products:", help="Type a product or keyword to filter messages.")
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
        st.dataframe(df_search, use_container_width=True)
        # Time series visualization
        if 'date' in df_search.columns and not df_search.empty:
            df_search['date'] = pd.to_datetime(df_search['date'])
            st.line_chart(df_search.groupby(df_search['date'].dt.date).size())
    except Exception as e:
        st.warning(f"Could not search messages: {e}")
    st.markdown('</div>', unsafe_allow_html=True)

elif task == "Top Mentioned Products":
    st.markdown('<div class="main-section">', unsafe_allow_html=True)
    st.markdown('<div class="section-header">🏆 Top Mentioned Products</div>', unsafe_allow_html=True)
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
    st.markdown('</div>', unsafe_allow_html=True)

elif task == "Channel Activity":
    st.markdown('<div class="main-section">', unsafe_allow_html=True)
    st.markdown('<div class="section-header">📊 Channel Activity</div>', unsafe_allow_html=True)
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
        st.dataframe(df_channels, use_container_width=True)
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
    st.markdown('</div>', unsafe_allow_html=True)


conn.close()