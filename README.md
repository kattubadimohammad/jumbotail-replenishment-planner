# Jumbotail Replenishment Planner

## Candidate

Kattubadi Mohammad

## Objective

Build a replenishment planner that generates purchase order suggestions while considering:

- Inventory Norm
- Safety Stock
- Open Purchase Orders
- Daily Run Rate
- Case Size Rounding
- Space Constraints
- Vendor MOV

## Folder Structure

data/
notebooks/
sql/
database/
output/
dashboard/

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