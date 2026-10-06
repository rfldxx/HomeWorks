-- Переход к 1NF: разбиваем повторяющиеся группы
DROP TABLE IF EXISTS orders_1nf CASCADE;

CREATE TABLE orders_1nf (
    order_id         INTEGER,
    order_date       DATE,
    customer_name    TEXT,
    customer_email   TEXT,
    customer_phone   TEXT,
    delivery_address TEXT,
    line_number      INTEGER,  -- номер строки разворота
    product_name     TEXT,
    product_price    INTEGER,
    product_quantity INTEGER,
    total_amount     INTEGER,
    status           TEXT
);

-- Разворачиваем списки товаров в отдельные строки
INSERT INTO orders_1nf
SELECT
    order_id,
    order_date,
    customer_name,
    customer_email,
    customer_phone,
    delivery_address,
    line_number,
    trim(name),
    trim(price)   ::INTEGER,
    trim(quantity)::INTEGER,
    total_amount, status
FROM orders_raw
CROSS JOIN unnest(
    string_to_array(product_names,      ','),
    string_to_array(product_prices,     ','),
    string_to_array(product_quantities, ',')
) WITH ORDINALITY AS t(name, price, quantity, line_number);
