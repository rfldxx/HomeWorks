CREATE MATERIALIZED VIEW mv_monthly_sales AS
SELECT
    date_trunc('month', order_date) AS month,
    date_trunc('year',  order_date) AS  year,
    product_name,
    SUM(product_quantity)                 AS total_quantity,
    SUM(product_quantity * product_price) AS total_revenue
FROM order_items 
JOIN orders       USING (     order_id)
JOIN order_phases USING (     order_id)
JOIN products     USING ( product_name)
WHERE status = 'completed'
GROUP BY 1, 2, 3;

EXPLAIN ANALYZE
SELECT *
FROM mv_monthly_sales
WHERE month >= '2024-01-01'
ORDER BY total_revenue DESC
LIMIT 10;

EXPLAIN ANALYZE
WITH monthly_sales AS (
    SELECT
        date_trunc('month', order_date) AS month,
        date_trunc('year',  order_date) AS  year,
        product_name,
        SUM(product_quantity)                 AS total_quantity,
        SUM(product_quantity * product_price) AS total_revenue
    FROM order_items 
    JOIN orders       USING (     order_id)
    JOIN order_phases USING (     order_id)
    JOIN products     USING ( product_name)
    WHERE status = 'completed'
    GROUP BY 1, 2, 3
)
SELECT *
FROM monthly_sales
WHERE month >= '2024-01-01'
ORDER BY total_revenue DESC
LIMIT 10;