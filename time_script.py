import psycopg2, time

conn = psycopg2.connect(
    host="localhost",
    port="5432",
    database="flaskapp_dev",
    user="flaskapp",
    password="flaskapp"
)
cur = conn.cursor()

query1 = """
SELECT * FROM supplier s
LEFT JOIN "order" o on s.id = o.supplier_id
WHERE
    (o.status = 'in_progress' OR o.status IS NULL)
    AND
    SQRT(POW(s.lat - 51.123, 2) + POW(s.lon - 47.123, 2)) < 0.05
GROUP BY s.id, s.lat, s.lon, o.id
HAVING COUNT(o.id) <= 5
ORDER BY SQRT(POW(s.lat - 51.123, 2) + POW(s.lon - 47.123, 2))
LIMIT 1
"""

query2 = """
WITH subquery AS (
    SELECT product_id,
           name,
           SUM(count)                 AS times_sold,
           price                      AS old_price,
           ROUND(106.8 * price) / 100 AS newprice
    FROM product
             JOIN order_item oi ON product.id = oi.product_id
             JOIN "order" o ON o.id = oi.order_id
    WHERE DATE_PART('year', date_ordered) = 2001
    GROUP BY product_id, name, price
    ORDER BY times_sold DESC
    LIMIT 1
)
UPDATE product
SET price = subquery.newprice
FROM subquery
WHERE product.id = subquery.product_id
"""

for i in range(10):
    start_time = time.time()
    cur.execute(query1)
    cur.fetchall()
    dt = time.time() - start_time
    print(dt)


print("-------------------------------")

for i in range(10):
    start_time = time.time()
    cur.execute(query2)
    conn.commit()
    dt = time.time() - start_time
    print(dt)
