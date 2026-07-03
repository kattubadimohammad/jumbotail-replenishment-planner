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
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "database" / "replenishment.db"

# ----------------------------------------
# Cached Database Operations
# ----------------------------------------
@st.cache_data
def load_raw_data(db_file):
    conn = sqlite3.connect(str(db_file))
    try:
        df = pd.read_sql("SELECT * FROM replenishment", conn)
        return df
    finally:
        conn.close()

if not DB_PATH.exists():
    st.error(f"📁 Database file could not be found at target destination: `{DB_PATH}`")
    st.stop()

# Load all data
df_raw = load_raw_data(DB_PATH)

# ----------------------------------------
# Sidebar Filters (APM Operational Enhancements)
# ----------------------------------------
st.sidebar.header("🎯 Dashboard Filters")

# Category Filter
categories = ["All Categories"] + sorted(df_raw["category_name"].dropna().unique().tolist())
selected_category = st.sidebar.selectbox("Filter by Category", categories)

# Apply filter to dataframe
if selected_category != "All Categories":
    df_filtered = df_raw[df_raw["category_name"] == selected_category]
else:
    df_filtered = df_raw.copy()

# ----------------------------------------
# Summary Metrics
# ----------------------------------------
st.header("Summary")
col1, col2, col3 = st.columns(3)

total_skus = len(df_filtered)
total_units = int(df_filtered["final_suggestion"].sum())
total_value = df_filtered["final_value"].sum()

col1.metric("Total SKUs", f"{total_skus:,}")
col2.metric("Total Suggested Units", f"{total_units:,}")
col3.metric("Total Order Value", f"₹ {total_value:,.2f}")

st.divider()

# ----------------------------------------
# Visualizations Data Preparation
# ----------------------------------------
# 1. Category-wise Aggregation
category_data = df_filtered.groupby("category_name")["final_value"].sum().reset_index()
category_data = category_data.sort_values(by="final_value", ascending=False).set_index("category_name")

# 2. Top 10 Vendors Aggregation
vendor_data = df_filtered.groupby("vendor_name")["final_value"].sum().reset_index()
vendor_data = vendor_data.sort_values(by="final_value", ascending=True).tail(10).set_index("vendor_name")

# 3. Top 10 SKUs Aggregation
sku_data = df_filtered[df_filtered["final_suggestion"] > 0]
sku_data = sku_data.groupby("title")["final_suggestion"].sum().reset_index()
sku_data = sku_data.sort_values(by="final_suggestion", ascending=True).tail(10).set_index("title")

# ----------------------------------------
# Render Dashboard Charts
# ----------------------------------------
col_left, col_right = st.columns(2)

with col_left:
    st.header("Category-wise Order Value")
    st.bar_chart(
        category_data, 
        y="final_value", 
        color="#FF4B4B",
        y_label="Total Order Value (₹)"
    )

with col_right:
    st.header("Top 10 Vendors")
    st.bar_chart(
        vendor_data, 
        y="final_value", 
        horizontal=True, 
        color="#FF4B4B",
        x_label="Total Order Value (₹)"
    )

st.divider()

st.header("Top 10 Replenishment Required SKUs")
st.bar_chart(
    sku_data, 
    y="final_suggestion", 
    horizontal=True, 
    color="#29B5E8",
    x_label="Suggested Order Quantity (Units)"
)

# ----------------------------------------
# Raw Data Expansion (Great for APM Reviews)
# ----------------------------------------
st.divider()
with st.expander("🔍 Inspect Filtered Replenishment Records"):
    st.dataframe(
        df_filtered[["title", "category_name", "vendor_name", "final_suggestion", "final_value"]],
        use_container_width=True
    )

# ----------------------------------------
# Footer
# ----------------------------------------
st.caption(
    "Developed by Kattubadi Mohammad | Associate Programme Manager Assignment"
)
