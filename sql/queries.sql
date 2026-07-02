-- Query 1: Category-wise Suggested Order Value

SELECT
    category_name,
    SUM(final_value) AS total_order_value
FROM replenishment
GROUP BY category_name
ORDER BY total_order_value DESC;


-- Query 2: Vendor-wise Suggested Order Summary

SELECT
    vendor_name,
    SUM(final_value) AS total_order_value,
    SUM(final_suggestion) AS total_units
FROM replenishment
GROUP BY vendor_name
ORDER BY total_order_value DESC;