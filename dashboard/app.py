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
# Sidebar Filters (Multi-Filter Setup)
# ----------------------------------------
st.sidebar.header("🎯 Operational Control")

# 1. Category Filter
categories = ["All Categories"] + sorted(df_raw["category_name"].dropna().unique().tolist())
selected_category = st.sidebar.selectbox("Filter by Category", categories)

# Filter dataframe by category first to make the vendor list dynamic
if selected_category != "All Categories":
    df_step = df_raw[df_raw["category_name"] == selected_category]
else:
    df_step = df_raw.copy()

# 2. Vendor Filter (Updates dynamically based on selected category)
vendors = ["All Vendors"] + sorted(df_step["vendor_name"].dropna().unique().tolist())
selected_vendor = st.sidebar.selectbox("Filter by Vendor", vendors)

# Apply final vendor filter
if selected_vendor != "All Vendors":
    df_filtered = df_step[df_step["vendor_name"] == selected_vendor]
else:
    df_filtered = df_step.copy()

# ----------------------------------------
# Summary Metrics & Operational Insights
# ----------------------------------------
st.header("Summary")

# Custom column ratios [1, 1, 1.3, 1] give the currency metric more space to prevent truncation
col1, col2, col3, col4 = st.columns([1, 1, 1.3, 1])

total_skus = len(df_filtered)
total_units = int(df_filtered["final_suggestion"].sum())
total_value = df_filtered["final_value"].sum()

# Critical SKUs (Items where replenishment suggestion is exceptionally high)
high_urgency_threshold = df_raw["final_suggestion"].quantile(0.90) if not df_raw.empty else 0
critical_skus = len(df_filtered[df_filtered["final_suggestion"] >= high_urgency_threshold])

col1.metric("Total SKUs Managed", f"{total_skus:,}")
col2.metric("Total Suggested Units", f"{total_units:,}")
col3.metric("Total Order Value", f"₹ {total_value:,.2f}")
col4.metric("🚨 High Urgency SKUs", f"{critical_skus:,}", help="SKUs in the top 10% of required replenishment quantities.")

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
    if not category_data.empty:
        st.bar_chart(category_data, y="final_value", color="#FF4B4B", y_label="Total Order Value (₹)")
    else:
        st.info("No data available for the current selection.")

with col_right:
    st.header("Top 10 Vendors")
    if not vendor_data.empty:
        st.bar_chart(vendor_data, y="final_value", horizontal=True, color="#FF4B4B", x_label="Total Order Value (₹)")
    else:
        st.info("No data available for the current selection.")

st.divider()

st.header("Top 10 Replenishment Required SKUs")
if not sku_data.empty:
    st.bar_chart(sku_data, y="final_suggestion", horizontal=True, color="#29B5E8", x_label="Suggested Order Quantity (Units)")
else:
    st.info("No SKUs currently require replenishment under these filter parameters.")

# ----------------------------------------
# Actionable Data Export (The Procurement Desk)
# ----------------------------------------
st.divider()
st.header("📋 Procurement Execution Desk")

# Cleaned up data format for professional presentation
df_display = df_filtered[["title", "category_name", "vendor_name", "final_suggestion", "final_value"]].rename(
    columns={
        "title": "Product Title",
        "category_name": "Category",
        "vendor_name": "Vendor",
        "final_suggestion": "Suggested Quantity (Units)",
        "final_value": "Order Value (INR)"
    }
)

# Render operational actions
col_meta, col_btn = st.columns([4, 1])
with col_meta:
    st.write(f"Showing **{len(df_display)}** item lines matching current selection criteria.")

with col_btn:
    csv_data = df_display.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Export PO Data (CSV)",
        data=csv_data,
        file_name="jumbotail_replenishment_orders.csv",
        mime="text/csv",
        use_container_width=True
    )

with st.expander("🔍 Click to Expand and Inspect Full Line-Item Breakdown"):
    st.dataframe(df_display, use_container_width=True)

# ----------------------------------------
# Footer
# ----------------------------------------
st.caption(
    "Developed by Kattubadi Mohammad | Associate Programme Manager Assignment"
)
