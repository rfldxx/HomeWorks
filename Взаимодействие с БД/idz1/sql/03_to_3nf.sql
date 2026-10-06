DROP TABLE IF EXISTS order_items   CASCADE;
DROP TABLE IF EXISTS order_phases  CASCADE;
DROP TABLE IF EXISTS orders        CASCADE;
DROP TABLE IF EXISTS products      CASCADE;
DROP TABLE IF EXISTS customers     CASCADE;


CREATE TABLE customers (
    customer_id    SERIAL PRIMARY KEY,
    customer_name  TEXT,
    customer_email TEXT,
    customer_phone TEXT
);


CREATE TABLE orders (
    order_id         SERIAL  PRIMARY KEY,
    customer_id      INTEGER REFERENCES customers(customer_id),
    delivery_address TEXT,
    total_amount     INTEGER
);

CREATE TABLE order_phases (
    order_id   INTEGER REFERENCES orders(order_id),
    status     TEXT,
    order_date DATE,
    PRIMARY KEY (order_id, status)
);

CREATE TABLE products (
    product_name  TEXT    PRIMARY KEY,
    product_price INTEGER
);

CREATE TABLE order_items (
    order_id         INTEGER REFERENCES orders  (order_id),
    product_name     TEXT    REFERENCES products(product_name),
    product_quantity INTEGER,
    PRIMARY KEY (order_id, product_name)
);

---------------------------------------------------------------------------------------------------

INSERT INTO customers (customer_name, customer_email, customer_phone)
SELECT DISTINCT customer_name, customer_email, customer_phone
FROM orders_2nf;

INSERT INTO orders
SELECT order_id, customer_id, delivery_address, total_amount
FROM orders_2nf
NATURAL JOIN customers;

-- чтобы SERIAL назначился правильно
SELECT setval( pg_get_serial_sequence('orders', 'order_id'), (SELECT MAX(order_id) FROM orders) );


-- полное копирование
INSERT INTO order_phases
SELECT *
FROM order_phases_2nf;

INSERT INTO products
SELECT *
FROM products_2nf;

INSERT INTO order_items
SELECT *
FROM order_items_2nf;



