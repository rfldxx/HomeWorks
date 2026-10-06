-- FK
CREATE INDEX idx_orders_customer_id 
ON orders(customer_id);

CREATE INDEX idx_order_items_product_name
ON order_items(product_name);

-- email
CREATE INDEX idx_customers_email
ON customers(customer_email);


-- вызов EXPLAIN ANALYZE для старых запросов

-- email : GIN +
CREATE EXTENSION IF NOT EXISTS pg_trgm;

CREATE INDEX idx_customers_email_trgm
ON customers
USING GIN (customer_email gin_trgm_ops);


-- вызов EXPLAIN ANALYZE для старых запросов

