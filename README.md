# 📦 Jumbotail Replenishment Planner

## 👤 Candidate Details
* **Name:** Kattubadi Mohammad
* **Position:** Associate Programme Manager Assignment

---

## 🎯 Project Objective
The objective of this project is to build an end-to-end automated supply chain replenishment planner that transforms raw inventory metrics into optimized purchase order (PO) recommendations. The planning logic systematically accounts for critical warehouse and procurement constraints:
* **Inventory Norms & Safety Stock levels** to mitigate stockouts.
* **Open Purchase Orders** to prevent redundant capital lock-up.
* **Daily Run Rate (DRR)** to match actual consumption trends.
* **Case Size Rounding** to ensure operational feasibility at supplier docks.
* **Warehouse Space Constraints** to prevent physical over-capacity issues.
* **Vendor Minimum Order Value (MOV)** thresholds to optimize procurement logistics.

---

## 📂 Repository Structure
```text
jumbotail-replenishment-planner/
├── dashboard/          # Production-ready Streamlit application layer (app.py)
├── data/               # Raw input datasets (inventory, sales, vendors)
├── database/           # SQLite relational storage layer (replenishment.db)
├── notebooks/          # Jupyter Notebooks for ETL & algorithm prototyping
├── reports/            # Generated flat-file procurement reports
└── sql/                # Core analytical queries for operational tracking

🛠️ Installation & Setup
Clone the Repository:

Bash
git clone [https://github.com/kattubadimohammad/jumbotail-replenishment-planner.git](https://github.com/kattubadimohammad/jumbotail-replenishment-planner.git)
cd jumbotail-replenishment-planner
Install Dependencies:
Ensure you have Python 3.8+ installed, then run:

Bash
pip install -r requirements.txt
🚀 Execution Workflow
Step 1: Data Pipeline Execution
Open and execute the data pipeline notebook to clear old staging tables, process raw logs, and populate the backend database:

Target File: notebooks/replenishment_planner.ipynb

Run all cells to update the inventory metrics and generate automated tables.

Step 2: Launch the Analytics Dashboard
Run the production web interface locally to visually inspect, filter, and export the generated purchase orders:

Bash
streamlit run dashboard/app.py
📊 Core Deliverables & Artifacts
reports/replenishment_output.csv – Structured flat-file data export for direct cross-functional sharing.

database/replenishment.db – Local SQLite database housing clean relational tables built from the ETL sequence.

sql/queries.sql – Production analytical queries designed to audit fulfillment health metrics and vendor distribution profiles.

Interactive Replenishment Dashboard – A fully deployed cloud interface on Streamlit Cloud featuring:

Dynamic Dependent Dropdowns: Filter metrics simultaneously by Category and Vendor.

Automated Data Caching: Employs @st.cache_data for performance optimization and ultra-low database query latency.

Procurement Execution Desk: Expandable row-level drill-down table with an integrated Export PO to CSV button to streamline procurement pipelines.

📐 Planning Assumptions & Core Logic
Planning Horizon Baseline: 16 March 2026.

Logistics Alignment: Suggestions are calculated at the SKU level and automatically rounded up to match exact supplier case configurations.

Capacity Safeguards: Recommended inbound volumes are programmatically checked against maximum cubic warehouse constraints.

Pipeline Visibility: Incoming stock from active, unfulfilled POs is treated as incoming supply to prevent over-ordering.

🔮 Future Roadmap & Scalability
Predictive Demand Forecasting: Integrate predictive models (such as XGBoost or ARIMA) to replace static DRR metrics with seasonal trend forecasts.

Automated Vendor Notification Desk: Wire the execution desk directly into an SMTP/API pipeline to email purchase orders to suppliers with a single click.

Multi-Warehouse Support: Abstract the database structure to manage distribution centers across multiple regional geographies simultaneously.
