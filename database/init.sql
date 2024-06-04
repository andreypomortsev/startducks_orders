CREATE TABLE in_stock (
    ingredient VARCHAR(50) PRIMARY KEY,
    quantity INT NOT NULL
);

INSERT INTO in_stock (ingredient, quantity) VALUES
('coffee', 100),
('milk', 100),
('cream', 100);
