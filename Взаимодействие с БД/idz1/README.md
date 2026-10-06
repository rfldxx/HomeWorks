# ИДЗ-1. PostgreSQL: структуры данных, нормализация и денормализация

Код можно запускать онлайн: https://playcode.io/sql-template (регистрация не нужна, но нужно vpn).



## Часть 1. Ненормализованная таблица (UNF)

Изначально есть "плоская" таблица `orders_raw`, имитирующую выгрузку из Excel.

```sql
CREATE TABLE orders_raw (
    order_id           INTEGER,
    order_date         DATE,
    customer_name      TEXT,       -- "Иванов Иван Иванович"
    customer_email     TEXT,
    customer_phone     TEXT,
    delivery_address   TEXT,
    product_names      TEXT,       -- "Ноутбук, Мышь, Коврик"
    product_prices     TEXT,       -- "85000, 1500, 500"
    product_quantities TEXT,       -- "1, 1, 2"
    total_amount       NUMERIC,
    status             TEXT        -- "delivered"
);
```
Уточним:

* Цена определенного товара фиксированна и не меняется.

* Каждому заказу выдаётся уникальный `order_id`.

* Заказ проходит разные `status` ("booked" -> "paided" -> "shipped" -> "completed" / "cancelled"), при этом возможно меняется `order_date`. \
    В сырой таблице это реализовано повторением строк:
    | order_id | order_date | ... | status |
    |---|---|---|---|
    |333| '2026-01-10' | одинаково |"booked"|
    |333| '2026-01-10' | одинаково |"paided"|
    |333| '2026-01-23' | одинаково |"shipped"|


### Генерация данных
Код для генерации таблицы: [scripts/generate_data.cpp](scripts/generate_data.cpp). \
В результате его выполнения напечатается готовый sql скрипт, который помещён в: [sql/00_orders_raw.sql](sql/00_orders_raw.sql). 

Даты в коде создаются с помощью: `DATE '2020-01-01' + 500` (к дате можно прибавлять/вычитать дни). \
Также из интересного: `DATE - DATE = число дней`.

Особенности генерации:
* `order_id` с пропусками,
* порядок строк перемешан,
* создаётся цепочка записей по `status` с возрастающими `order_date`,
* в строке `product_names` товары могут повторяться, `product_quantities` могут равняться нулю (чтобы потом было по интереснее с запросами).

### Аномалии

Аномалии появляются из-за избыточности данных: один и тот же факт хранится в нескольких строках или, наоборот, связанные факты нельзя хранить отдельно.

**Аномалия вставки.** Нельзя добавить новый товар в справочник, не создав при этом заказ. Информация о товаре и его цене существует только внутри строки заказа.

**Аномалия обновления.** При изменении цены товара нужно обновить её во всех строках, где этот товар упоминается.

**Аномалия удаления.** При удалении последнего заказа с товаром исчезает и информация о самом товаре.


## Часть 2. Нормализация до 3NF

Нормализация помогает привести базу данных к виду обеспечивающему минимальную логическую избыточность.

Можно найти конспекты:
* [Цели и средства нормализации](https://neerc.ifmo.ru/wiki/index.php?title=Цели_и_средства_нормализации),
* [Нормальные формы: первая и вторая](https://neerc.ifmo.ru/wiki/index.php?title=Нормальные_формы:_первая_и_вторая),
* [Нормальные формы: третья и Бойса-Кодда](https://neerc.ifmo.ru/wiki/index.php?title=Нормальные_формы:_третья_и_Бойса-Кодда).

Функциональная зависимость (FD): $X \rightarrow Y$. \
Пусть дана схема отношения $R(U)$, где $U$ — множество атрибутов. \
Ключ-кандидат - минимальное множество атрибутов $K$, такое что: $K \rightarrow U$.

Полные SQL скрипты лежат в: `01_to_1nf.sql`, `02_to_2nf.sql`, `03_to_3nf.sql`.

### 1NF — атомарность

Требуется:
* в отношении нет повторяющихся групп (атрибутов с одинаковым смыслом),
* все атрибуты атомарны,
* у отношения есть ключ.

Первая проблема, что столбцы: `product_names`, `product_prices`, `product_quantities` не атомарны. \
Их можно синхроно развернуть:
```sql
SELECT
    trim(UNNEST(string_to_array(product_names,      ','))),
    trim(UNNEST(string_to_array(product_prices,     ',')))::INTEGER,
    trim(UNNEST(string_to_array(product_quantities, ',')))::INTEGER
FROM orders_raw;
```
Основную работу делает `UNNEST` - это Set Returning Function (**SRF**), которая разворачивает массив (или несколько массивов) в набор строк. \
Начиная с PostgreSQL 10 результаты **SRF** в `SELECT` раскрываются синхронно («lock-step»).


Однако в исходных данных в одном `product_names` могут быть повторы товаров. После разворота массива могут возникнуть повторы строк (если окажутся равны соответсвующие `product_quantities`, `product_prices`). \
Но 1NF должно быть множеством - значит не должно быть повторов.


Чтобы минимальными усилиями добиться 1NF, введём атрибут `line_number` - индекс позиции в массиве.
```sql
SELECT
    line_number,
    trim(name),
    trim(price)   ::INTEGER,
    trim(quantity)::INTEGER
FROM orders_raw
CROSS JOIN unnest(
    string_to_array(product_names,      ','),
    string_to_array(product_prices,     ','),
    string_to_array(product_quantities, ',')
) WITH ORDINALITY AS t(name, price, quantity, line_number);
```

КСТАТИ: PostgreSQL вызывает функцию `unnest` для каждой строки отдельно. Формальео стоило написать **LATERAL**, подробнее про LATERAL будет в: [3. Получение заказа](#3-получение-заказа).

Ключом в итоговой `orders_1nf` является: `(order_id, status, line_number)`.

### 2NF — устранение частичных зависимостей
Дополнительно требуется:
* Каждый неключевые атрибут функционально зависит (FD) от каждого ключа-кандидата полностью (а не от части ключа-кандидата).

Давайте при рассмотрении избавимся от суррогатного атрибута `line_number`, просуммировав одинаковые товары в пределах одного заказа. \
Тогда ключом будет тройка: `(order_id, status, product_name)`.


У нас есть FD связанные только с **частью** ключа-кандидата:
```
 order_id                -> customer_name, customer_email, customer_phone, delivery_address, total_amount
(order_id,       status) -> order_date
(order_id, product_name) -> product_quantity
           product_name  -> product_price
```

Проведём декомпозицию на следующие таблицы:

```sql
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
```

При вставки из `orders_1nf` главное не забывать писать `DISTINCT`. \
Самый содержательный запрос был связан с "агрегацией" одинаковых товаров в одном заказе:
```sql
INSERT INTO order_items_2nf
SELECT DISTINCT ON (order_id, product_name)
    order_id,
    product_name,
    SUM(product_quantity)
FROM orders_1nf
GROUP BY order_id, status, product_name
HAVING SUM(product_quantity) > 0;
```



### 3NF — устранение транзитивных зависимостей
Дополнительно требуется:
* Для каждой нетривиальной FD $X \rightarrow A$, где $A$ — одиночный атрибут, должно выполняться хотя бы одно:
    - $X$ — суперключ (любое множество атрибутов, содержащее ключ-кандидат),
    - $A$ — простой атрибут (атрибут, который входит хотя бы в один ключ-кандидат).


Рассмотрим покупателя, могут быть два вариант:
* человек характерезуется тройкой `(name, phone, email)`. То тогда таблицы с шага 2NF уже **формально** удовлетворяют 3NF.\
    Однако всё равно остаются аномалии при редактировании пользователя. 

* человек характерезуется только частью аргументов, например только по `email`. То тогда возникает транзиктивная зависимость: `order_id -> email`, `email -> name, phone`.

Решением в обоих случаях является создание отдельной таблицы `customers` и нового атрибута `customer_id`:
```sql
CREATE TABLE customers (
    customer_id    SERIAL PRIMARY KEY,
    customer_name  TEXT,
    customer_email TEXT,
    customer_phone TEXT
);
```

Давайте для будущего удобства сделаем `order_id` тоже `SERIAL`. Но возникает одна деталь. \
На самом деле `SERIAL` по сути макрос, который раскрывается в отдельную последовательность `CREATE SEQUENCE seq AS INTEGER` и из которой берётся `nextval('seq')` в случае если поле не задано. \
Поэтому когда мы вставляем элементы с известным `order_id`, то `nextval('seq')` не вызывается! Поэтому после после миграции надо сделать:
```sql
SELECT setval( pg_get_serial_sequence('orders', 'order_id'), (SELECT MAX(order_id) FROM orders) );
```

Ещё, если вдруг исходня таблица пуста, то `MAX(order_id)` вернёт `NULL`. Это можно починить:
```sql
SELECT COALESCE(MAX(order_id), 0) FROM orders;
```

Итоговая ER-диаграмма в PlantUML: [schema.puml](schema.puml).



## Часть 3. OLTP-нагрузка на нормализованной схеме

OLTP (Online Transaction Processing) - класс нагрузки, при котором система обрабатывает много коротких транзакций в реальном времени. Например, пользователь нажал кнопку - заказ создан, статус обновлён, страница загрузилась.

В этом случае есть опасность гонки данных.

Все OLTP-запросы: `04_oltp_queries.sql`. 

### 1. Создание заказа

Операция `nextval()` (которая вызывается из `SERIAL`) - атомарная. Поэтому не будет проблем при автоматичском назначении `order_id`.

С таблицой `products` сложнее: сначала мы читаем от туда данные, затем вычисляем `total_amount`, зачем пишем в таблицу `orders`. И надо чтобы выбранные цены не менялись, иначе будет рассинхронизация данных.

Конструкция: `SELECT ... FOR UPDATE` - это обычный `SELECT`, который дополнительно блокирует выбранные строки до конца текущей транзакции. Любая другая транзакция, которая попытается сделать `UPDATE`, `DELETE` или `SELECT ... FOR UPDATE` по этим же строкам, будет ждать окончания нашей транзакции.

Также удобные возможности:
* В CTE можно использовать `INSERT INTO ... RETURNING`, чтобы вернуть автосгенирированный `order_id`,

* `A JOIN B USING (c1, c2)` - объединяет таблицы `A` и `B` по указанным столбцам с одинаковым названием (вместо `A JOIN B ON A.c1 = B.c1 and A.c2 = B.c2`).

<details>

<summary> SQL-запрос </summary>

```sql
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
```

</details>


### 2. Обновление статуса
В задании требуется обновить `status`.

Интересно что `status` входит в PK, т.е. является индексированным! Соответственно обновление `status` вызывает некую работу с индексами, что заметно сложнее чем просто обновление "обычных" данных.

Если бы на `status` ссылась бы другая таблица через FK, то обычный `UPDATE` упал бы:
```
ERROR: update or delete on table "order_phases" violates
       foreign key constraint on table "other_table"
DETAIL: Key (order_id, status)=(2086, booked) is still referenced from table "other_table".
```
Причина: PostgreSQL по умолчанию использует `ON UPDATE NO ACTION` - он запрещает менять значение PK, пока на него кто-то ссылается. \
Для решения в объявлениии `FOREIGN KEY` можно было бы указать `ON UPDATE CASCADE` - тогда бы происходило автоматическое обновление FK во всех ссылающихся строках.





### 3. Получение заказа

В таблице для заказа хранится история: какие статусы он проходил. Выберем статус с самой большой датой.

```sql
-- Вариант 1. 
SELECT *
FROM orders
NATURAL JOIN customers
NATURAL JOIN order_items
NATURAL JOIN products
NATURAL JOIN (
    SELECT
        order_id,
        status     AS last_status,
        order_date AS status_date
    FROM order_phases
    WHERE order_id = 333
    ORDER BY order_date DESC
    LIMIT 1
)
WHERE order_id = 333
```

Однако приходятся указывать `order_id` в двух местах. \
К томе же, если вдруг на `order_id` будет наложенно сложное условие, то придется подумать как модифицировать запрос.

Здесь поможет `CROSS JOIN LATERAL`. Формально:
* Обычный `CROSS JOIN`: $A \times B$, где $B$ — фиксированное множество (одно и то же для всех $a \in A$). 
* С **LATERAL**: $\bigcup_{a \in A} \set{a} \times B(a)$, где $B(a)$ — результат подзапроса для конкретной строки $a$.

```sql
-- Вариант 2. 
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
```

Почему LATERAL стоит до `order_items`? **LATERAL** вычисляется для **каждой строки
того, что слева**. \
Если поставить LATERAL после `JOIN` с `order_items`, то LATERAL будет вычисляться для каждой позиции в заказе (в одном заказе их может быть несколько). А в первом варианте подзапрос был независимым и мог располагаться где угодно.

### 4. Отчёт "топ-10 товаров"
```sql
SELECT
    product_name,
    SUM(product_quantity)                 AS total_sold,
    SUM(product_quantity * product_price) AS revenue
FROM order_items
NATURAL JOIN products
GROUP BY product_name
ORDER BY revenue DESC
LIMIT 10;
```

### 5. Поиск клиента
```sql
SELECT *
FROM customers
WHERE customer_id = 444;

SELECT *
FROM customers
WHERE customer_email = 'rena1975@gmail.com';

SELECT *
FROM customers
WHERE customer_email LIKE '%rena%';
```



## Часть 4. Денормализация

### 4.1. Материализованное представление для отчётов

Материализованное представление `MATERIALIZED VIEW` - это физическая сохраненная таблица, в которую положен результат запроса. \
Данные в ней не поддерживаются актуальными. Для полного пересчёта можно вызвать `REFRESH`.

<details>

<summary> SQL-запрос </summary>

```sql
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
```
</details>

Понятно так как таблица создана, то при запросах не тратятся "ресурсы" на объединение, группировку и прочие "подготовительные" действия.

Сравнение EXPLAIN на MV и JOIN: [checks/mv_vs_join.txt](checks/mv_vs_join.txt).


### 4.2. Денормализация в таблицу

Добавить избыточное поле.

```sql
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
```

Это создает избыточность в базе, и аномалии обновления/удаления.

Однако, так как данные храняться по строчно, такая колонка может значительно уменьшить число обращений в память при запросах, чем полностью нормализованная таблица.

Также, аномалия обновления может сыграть и в плюс - у нас будет оставаться старое значение, a.k.a исторический снимок.



## Часть 5. Индексы

Надо сделать индексацию для запроса: "5. Поиск клиента по email." \
В остальных запросах `JOIN` ведётся по PK, а он уже индексирован.


FK: PostgreSQL **не создаёт** индексы для FK автоматически. \
Что может повлиять на запросы где надо по PK родителя найти все FK ссылающиеса на него. Например:
* удаление и обновление PK родителя,
* `JOIN` "родитель" -> "дети"
* и т. д.


Из-за того что B-tree по сути сортирует лексико-графически, то можно эффективно искать префикс составного ключа. \
Если в B-tree  находится строка, то по той же логике, мы можем эффективно искать строки по префексу.

```sql
-- email
CREATE INDEX idx_customers_email
ON customers(customer_email);

-- FK
CREATE INDEX idx_orders_customer_id 
ON orders(customer_id);

CREATE INDEX idx_order_items_product_name
ON order_items(product_name);
```


Однако остаётся проблема с поиском строки: `LIKE '%text%'`. \
Выполнение таких запросов можно ускорить с помощью GIN (Generalized Inverted Index). [Про GIN индексы](https://habr.com/ru/companies/postgrespro/articles/340978/). \
GIN работает с типами данных, значения которых не являются атомарными, а состоят из элементов. При этом индексируются не сами значения, а отдельные элементы; каждый элемент ссылается на те значения, в которых он встречается.

Для строк есть возможность индексировать триграммы (группы из трёх последовательных символов) через `pg_trgm`. \
При поиске строки по шаблону, сначала происходит отбор строк которые содержат все триграммы из шаблона. Затем найденные строки сравниваются с шаблоном.

```sql
-- email: GIN + pg_trgm
CREATE EXTENSION IF NOT EXISTS pg_trgm;

CREATE INDEX idx_customers_email_trgm
ON customers
USING GIN (customer_email gin_trgm_ops);
```

Результат EXPLAIN до индексов: [checks/explain_before_idx.txt](checks/explain_before_idx.txt). \
Результат EXPLAIN после индексов: [checks/explain_after_idx.txt](checks/explain_after_idx.txt).

## Часть 6. Сравнительная таблица OLTP vs OLAP

OLTP, Online Transaction Processing, Оперативная обработка транзакций. \
OLAP, Online Analytical Processing, Оперативная аналитическая обработка.

| Характеристика | OLTP (PostgreSQL) | OLAP (ClickHouse) |
|---|---|---|
| **Модель хранения** | Строковая. Данные одной строки хранятся вместе. Оптимально для точечных операций с целыми строками. | Колоночная. Данные одного столбца хранятся вместе. Читаются только нужные столбцы. |
| **Типичный запрос** | Точечные: получить/изменить несколько строк по ключу. Много коротких транзакций. | Аналитические: `SUM`, `COUNT`, `GROUP BY`, временные ряды по миллиардам строк. |
| **Нормализация** | Высокая (3НФ и выше). Цель - устранить избыточность и аномалии обновления. | Низкая (денормализация). Широкие «плоские» таблицы для минимизации `JOIN`. |
| **Транзакции** | Полная поддержка ACID. | Ограниченная. Нет полноценных транзакций с `ROLLBACK`. |
| **Вставка** | Частые одиночные вставки в транзакциях. Низкая latency, невысокий throughput. | Пакетная вставка. Огромный throughput, одиночные вставки неэффективны. |
| **Обновление/удаление** | Эффективны. Стандартные `UPDATE` и `DELETE`. | Крайне неэффективны. Асинхронные «мутации», перезаписывающие целые куски данных. |
| **Масштабирование** | Вертикальное (Scale-Up). Увеличение мощности одного сервера. | Горизонтальное (Scale-Out). Кластер из множества серверов. |
| **Типичный use case** | Бэкенды веб-приложений, интернет-магазины, банковские системы, ERP, CRM. | BI-дашборды, аналитика в реальном времени, обработка логов, телеметрия. |

## Структура репозитория

```
idz1/
├── README.md                  # аномалии, обоснования, таблица OLTP vs OLAP
├── schema.puml                # ER-диаграмма итоговой 3NF-схемы
├── sql/
│   ├── 00_orders_raw.sql      # UNF: создание + INSERT тестовых данных
│   ├── 01_to_1nf.sql          # миграция в 1NF
│   ├── 02_to_2nf.sql          # миграция в 2NF
│   ├── 03_to_3nf.sql          # миграция в 3NF
│   ├── 04_oltp_queries.sql    # OLTP-запросы
│   ├── 05_denorm_mv.sql       # материализованное представление
│   ├── 06_denorm_table.sql    # денормализация в таблицу
│   └── 07_indexes.sql         # создание индексов
├── scripts/
│   └── generate_data.cpp      # генерация тестовых данных
└── checks/
    ├── explain_before_idx.txt  # EXPLAIN до индексов
    ├── explain_after_idx.txt   # EXPLAIN после индексов
    └── mv_vs_join.txt          # сравнение MV и JOIN
```
