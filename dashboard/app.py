import streamlit as st
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt

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
# Connect SQLite Database
# ----------------------------------------
conn = sqlite3.connect("../database/replenishment.db")

df = pd.read_sql(
    "SELECT * FROM replenishment",
    conn
)

# ----------------------------------------
# Summary
# ----------------------------------------
st.header("Summary")

col1, col2, col3 = st.columns(3)

col1.metric(
    "Total SKUs",
    len(df)
)

col2.metric(
    "Total Suggested Units",
    int(df["final_suggestion"].sum())
)

col3.metric(
    "Total Order Value",
    f"₹ {df['final_value'].sum():,.2f}"
)

st.divider()

# ----------------------------------------
# Category-wise Order Value
# ----------------------------------------
st.header("Category-wise Order Value")

category = pd.read_sql("""
SELECT
    category_name,
    SUM(final_value) AS total_order_value
FROM replenishment
GROUP BY category_name
ORDER BY total_order_value DESC
""", conn)

fig1, ax1 = plt.subplots(figsize=(12,6))

ax1.bar(
    category["category_name"],
    category["total_order_value"]
)

ax1.set_title("Category-wise Suggested Order Value")
ax1.set_xlabel("Category")
ax1.set_ylabel("Order Value")

plt.xticks(rotation=35, ha="right")
plt.tight_layout()

st.pyplot(fig1)

st.divider()

# ----------------------------------------
# Top Vendors
# ----------------------------------------
st.header("Top 10 Vendors")

vendor = pd.read_sql("""
SELECT
    vendor_name,
    SUM(final_value) AS total_order_value
FROM replenishment
GROUP BY vendor_name
ORDER BY total_order_value DESC
LIMIT 10
""", conn)

fig2, ax2 = plt.subplots(figsize=(11,6))

ax2.barh(
    vendor["vendor_name"],
    vendor["total_order_value"]
)

ax2.invert_yaxis()

ax2.set_title("Top 10 Vendors")
ax2.set_xlabel("Suggested Order Value")

plt.tight_layout()

st.pyplot(fig2)

st.divider()

# ----------------------------------------
# Top Replenishment Required SKUs
# ----------------------------------------
st.header("Top 10 Replenishment Required SKUs")

risk = pd.read_sql("""
SELECT
    title,
    final_suggestion
FROM replenishment
WHERE final_suggestion > 0
ORDER BY final_suggestion DESC
LIMIT 10
""", conn)

fig3, ax3 = plt.subplots(figsize=(11,6))

ax3.barh(
    risk["title"],
    risk["final_suggestion"]
)

ax3.invert_yaxis()

ax3.set_title("Top 10 Replenishment Required SKUs")
ax3.set_xlabel("Suggested Order Quantity")

plt.tight_layout()

st.pyplot(fig3)

st.divider()

# ----------------------------------------
# Footer
# ----------------------------------------
st.caption(
    "Developed by Kattubadi Mohammad | Associate Programme Manager Assignment"
)

conn.close()