import streamlit as st
import pandas as pd
import sqlite3
from pathlib import Path

# ----------------------------------------
# Page Configuration
# ----------------------------------------
st.set_page_config(
    page_title="Jumbotail Replenishment Planner",
    page_icon="📦",
    layout="wide"
)

st.title("📦 Jumbotail Replenishment Planner")
st.caption("Purchase Order Recommendation Dashboard")

# ----------------------------------------
# Absolute Path Resolution
# ----------------------------------------
# This finds the exact directory of app.py, goes up one level, and finds the database
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "database" / "replenishment.db"

# ----------------------------------------
# Cached Database Operations
# ----------------------------------------
@st.cache_data
def load_dashboard_data(db_file):
    # Convert Path object to string for sqlite3 compatibility
    conn = sqlite3.connect(str(db_file))
    try:
        # Load main data for summary metrics
        df_summary = pd.read_sql("SELECT final_suggestion, final_value FROM replenishment", conn)
        total_skus = len(df_summary)
        total_units = int(df_summary["final_suggestion"].sum())
        total_value = df_summary["final_value"].sum()

        # Category-wise data
        df_category = pd.read_sql("""
            SELECT category_name, SUM(final_value) AS total_order_value 
            FROM replenishment 
            GROUP BY category_name 
            ORDER BY total_order_value DESC
        """, conn).set_index("category_name")

        # Top Vendors data
        df_vendor = pd.read_sql("""
            SELECT vendor_name, SUM(final_value) AS total_order_value 
            FROM replenishment 
            GROUP BY vendor_name 
            ORDER BY total_order_value DESC 
            LIMIT 10
        """, conn).set_index("vendor_name")

        # Top SKUs data
        df_skus = pd.read_sql("""
            SELECT title, final_suggestion 
            FROM replenishment 
            WHERE final_suggestion > 0 
            ORDER BY final_suggestion DESC 
            LIMIT 10
        """, conn).set_index("title")

        return total_skus, total_units, total_value, df_category, df_vendor, df_skus
    finally:
        conn.close()

# Safe data loading block
if not DB_PATH.exists():
    st.error(f"📁 Database file could not be found at target destination: `{DB_PATH}`")
    st.stop()

total_skus, total_units, total_value, category, vendor, risk = load_dashboard_data(DB_PATH)

# ----------------------------------------
# Summary Metrics
# ----------------------------------------
st.header("Summary")
col1, col2, col3 = st.columns(3)

col1.metric("Total SKUs", f"{total_skus:,}")
col2.metric("Total Suggested Units", f"{total_units:,}")
col3.metric("Total Order Value", f"₹ {total_value:,.2f}")

st.divider()

# ----------------------------------------
# Visualizations
# ----------------------------------------
col_left, col_right = st.columns(2)

with col_left:
    st.header("Category-wise Order Value")
    st.bar_chart(category, y="total_order_value", color="#FF4B4B")

with col_right:
    st.header("Top 10 Vendors")
    st.bar_chart(vendor, y="total_order_value", horizontal=True)

st.divider()

st.header("Top 10 Replenishment Required SKUs")
st.bar_chart(risk, y="final_suggestion", horizontal=True, color="#29B5E8")

st.divider()

# ----------------------------------------
# Footer
# ----------------------------------------
st.caption(
    "Developed by Kattubadi Mohammad | Associate Programme Manager Assignment"
)
