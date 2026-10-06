-- 1. Создание заказа

BEGIN;

EXPLAIN ANALYZE
WITH query AS (
    SELECT
        'Ноутбук, Кофемашина, Ноутбук, Холодильник' AS product_names,
        '1, 2, 1, 0'                                AS product_quantities,
        376                                         AS customer_id,
        'Санкт-Петербург, А'                        AS delivery_address,
        'booked'                                    AS status,
        CURRENT_DATE                                AS order_date
),
array_expanded AS (    -- разделили строку в таблицу
    SELECT
        TRIM(UNNEST(string_to_array(product_names,      ',')))          AS product_name,
        TRIM(UNNEST(string_to_array(product_quantities, ',')))::INTEGER AS quantity
    FROM query
),
query_agregated AS (   -- саккумулировали одинаковые товары
    SELECT
        product_name,
        SUM(quantity) AS product_quantity
    FROM array_expanded
    GROUP BY product_name
    HAVING SUM(quantity) > 0
),
locked_prices AS (
    SELECT
        product_name,
        product_price,
        product_quantity
    FROM products
    JOIN query_agregated USING (product_name)
    FOR UPDATE
),
new_order AS (
    INSERT INTO orders (customer_id, delivery_address, total_amount)
    SELECT
        customer_id,
        delivery_address,
        total_amount
    FROM query,
        (SELECT SUM(product_price * product_quantity) AS total_amount FROM locked_prices)
    RETURNING order_id AS new_order_id
),
new_order_phase AS (
    INSERT INTO order_phases (order_id, status, order_date)
    SELECT
        new_order_id,
        status,
        order_date
    FROM new_order, query
),
new_order_items AS (
    INSERT INTO order_items (order_id, product_name, product_quantity)
    SELECT
        new_order_id,
        product_name,
        product_quantity
    FROM locked_prices, new_order
)
SELECT new_order_id FROM new_order;

COMMIT;


---------------------------------------------------------------------------------------------------
-- 2. Обновление статуса

EXPLAIN ANALYZE
UPDATE order_phases
SET status = 'paided'
WHERE order_id = 2086 AND status = 'booked';


---------------------------------------------------------------------------------------------------
-- 3. Получение заказа

EXPLAIN ANALYZE
SELECT *
FROM orders
CROSS JOIN LATERAL (
    SELECT
        status     AS last_status,
        order_date AS status_date
    FROM order_phases
    WHERE order_id = orders.order_id
    ORDER BY order_date DESC
    LIMIT 1
)
NATURAL JOIN customers
NATURAL JOIN order_items
NATURAL JOIN products
WHERE order_id = 333;


---------------------------------------------------------------------------------------------------
-- 4. Отчёт "топ-10 товаров"

EXPLAIN ANALYZE
SELECT
    product_name,
    SUM(product_quantity)                 AS total_sold,
    SUM(product_quantity * product_price) AS revenue
FROM order_items
NATURAL JOIN products
GROUP BY product_name
ORDER BY revenue DESC
LIMIT 10;


---------------------------------------------------------------------------------------------------
-- 5. Поиск клиента
EXPLAIN ANALYZE
SELECT *
FROM customers
WHERE customer_id = 444;

EXPLAIN ANALYZE
SELECT *
FROM customers
WHERE customer_email = 'rena1975@gmail.com';

EXPLAIN ANALYZE
SELECT *
FROM customers
WHERE customer_email LIKE '%rena%';

