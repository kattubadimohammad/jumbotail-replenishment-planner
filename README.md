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

## Requirements

Install dependencies:

pip install -r requirements.txt

## Run Notebook

Open:

notebooks/replenishment_planner.ipynb

Execute all cells.

## Output

- replenishment_output.csv
- replenishment.db

## SQL

Two analytical SQL queries are included inside sql/queries.sql.

## Assumptions

- Planning date is 16 March 2026.
- Orders are rounded to case size.
- Storage capacity is respected.
- Open POs are considered.

## Future Improvements

- Demand Forecasting
- Streamlit Dashboard
- Automated Vendor PO Generation
