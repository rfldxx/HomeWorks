ALTER TABLE orders ADD COLUMN customer_name TEXT;
-- ALTER TABLE orders DROP COLUMN customer_name;

UPDATE orders
SET customer_name = customers.customer_name
FROM customers
WHERE customers.customer_id = orders.customer_id;

EXPLAIN ANALYZE
SELECT order_id, customer_name, total_amount 
FROM orders WHERE order_id = 333;

EXPLAIN ANALYZE
SELECT order_id, customer_name, total_amount
FROM orders JOIN customers USING (customer_id)
WHERE order_id = 333;