DROP TABLE IF EXISTS orders_2nf       CASCADE;
DROP TABLE IF EXISTS order_phases_2nf CASCADE;
DROP TABLE IF EXISTS order_items_2nf  CASCADE;
DROP TABLE IF EXISTS products_2nf     CASCADE;


CREATE TABLE orders_2nf (
    order_id         INTEGER PRIMARY KEY,
    customer_name    TEXT,
    customer_email   TEXT,
    customer_phone   TEXT,
    delivery_address TEXT,
    total_amount     INTEGER
);

CREATE TABLE order_phases_2nf (
    order_id   INTEGER REFERENCES orders_2nf(order_id),
    status     TEXT,
    order_date DATE,
    PRIMARY KEY (order_id, status)
);

CREATE TABLE products_2nf (
    product_name  TEXT    PRIMARY KEY,
    product_price INTEGER
);

CREATE TABLE order_items_2nf (
    order_id         INTEGER REFERENCES orders_2nf  (order_id),
    product_name     TEXT    REFERENCES products_2nf(product_name),
    product_quantity INTEGER,
    PRIMARY KEY (order_id, product_name)
);


-- DISTINCT - потому что заказы повторяется из-за "разворота" массивов
INSERT INTO orders_2nf
SELECT DISTINCT
    order_id,
    customer_name,
    customer_email,
    customer_phone,
    delivery_address,
    total_amount
FROM orders_1nf;


INSERT INTO order_phases_2nf
SELECT DISTINCT 
    order_id,
    status,
    order_date
FROM orders_1nf;


INSERT INTO products_2nf
SELECT DISTINCT
    product_name,
    product_price
FROM orders_1nf;


-- В генерации в одной строке product_names могут быть повторяющиеся товары
INSERT INTO order_items_2nf
SELECT DISTINCT ON (order_id, product_name)
    order_id,
    product_name,
    SUM(product_quantity)
FROM orders_1nf
GROUP BY order_id, status, product_name
HAVING SUM(product_quantity) > 0;