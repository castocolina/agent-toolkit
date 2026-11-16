-- SQLite 3.45, desktop point-of-sale app; one writer process.
-- The app opens every connection with PRAGMA foreign_keys = ON.

CREATE TABLE products (
  id INTEGER PRIMARY KEY,
  sku TEXT NOT NULL UNIQUE,
  name TEXT NOT NULL,
  price REAL NOT NULL,
  updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
CREATE INDEX idx_products_name ON products (name);
CREATE TRIGGER trg_products_touch AFTER UPDATE OF price ON products
BEGIN
  UPDATE products SET updated_at = CURRENT_TIMESTAMP WHERE id = NEW.id;
END;
CREATE VIEW product_list AS SELECT id, sku, name, price FROM products;

CREATE TABLE order_items (
  id INTEGER PRIMARY KEY,
  product_id INTEGER NOT NULL REFERENCES products (id),
  quantity INTEGER NOT NULL CHECK (quantity > 0),
  unit_price REAL NOT NULL
);
