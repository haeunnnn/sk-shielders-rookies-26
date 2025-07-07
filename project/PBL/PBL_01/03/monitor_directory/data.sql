SELECT * FROM users WHERE id = 1;
INSERT INTO products (name, price) VALUES ('Book', 20.00);
UPDATE orders SET status = 'shipped' WHERE order_id = 101;
DELETE FROM temp_data WHERE timestamp < '2023-01-01';
CREATE TABLE customers (id INT PRIMARY KEY, name VARCHAR(100));