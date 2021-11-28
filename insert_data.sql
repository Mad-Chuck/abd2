-- Run after database reset
TRUNCATE product RESTART IDENTITY CASCADE;
insert into product (name, description, price)
VALUES ('Samsung galaxy s20', 'Newest models from samsung s series.', 2999.99);
insert into product (name, description, price)
VALUES ('Iphone 13', 'The most expensive smartphone on market.', 4999.99);
insert into product (name, description, price)
VALUES ('ipad pro', 'Regular smartphone for big people.', 3999.99);
insert into product (name, price)
VALUES ('Huawei P30', 999.99);
insert into product (name, price)
VALUES ('Xiaomi 11', 1399.99);
insert into product (name, price)
VALUES ('Oppo 3', 599.99);
insert into product (name, price)
VALUES ('Redmi 10', 1200);

TRUNCATE consumer RESTART IDENTITY CASCADE;
insert into consumer (email, password, phone)
VALUES ('123@123.pl', '-4252508476332522232', '123123123');
insert into consumer (email, password, phone)
VALUES ('1234@1234.pl', '-9156641935121768956', '123412341234');


TRUNCATE supplier RESTART IDENTITY CASCADE;
insert into supplier (email, password, phone)
VALUES ('12345@12345.pl', '-3151639085879697209', '1234512345');

TRUNCATE "order" RESTART IDENTITY CASCADE;
insert into "order" (consumer_id, date_ordered, lat, lon, status)
VALUES (1, '2001-09-28 01:00:00', 51.123, 47.123, 'ordered');
insert into "order" (consumer_id, supplier_id, date_ordered, lat, lon, status)
VALUES (1, 1, '2001-09-28 01:00:00', 51.123, 47.123, 'in_progress');
insert into "order" (consumer_id, supplier_id, date_ordered, date_delivered, lat, lon, status)
VALUES (1, 1, '2001-09-28 01:00:00', '2002-09-28 01:00:00', 51.123, 47.123, 'delivered')


TRUNCATE order_item RESTART IDENTITY CASCADE;
insert into order_item (order_id, product_id, count, worth)
VALUES (1, 1, 1, 2999.99);
insert into order_item (order_id, product_id, count, worth)
VALUES (2, 2, 1, 2999.99);
insert into order_item (order_id, product_id, count, worth)
VALUES (3, 1, 2, 5999.98);