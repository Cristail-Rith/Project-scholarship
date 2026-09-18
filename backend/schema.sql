CREATE DATABASE IF NOT EXISTS restaurant_db
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE restaurant_db;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(80) NOT NULL UNIQUE,
    email VARCHAR(120) NOT NULL UNIQUE,
    password_hash VARCHAR(256) NOT NULL,
    role VARCHAR(20) NOT NULL DEFAULT 'customer',
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(80) NOT NULL UNIQUE,
    slug VARCHAR(120) NOT NULL DEFAULT '',
    description TEXT NOT NULL,
    image VARCHAR(500) NOT NULL DEFAULT '',
    icon VARCHAR(40) NOT NULL DEFAULT 'utensils',
    station VARCHAR(80) NOT NULL DEFAULT 'Main Line',
    status VARCHAR(20) NOT NULL DEFAULT 'Active',
    display_order INT NOT NULL DEFAULT 1
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(120) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    previous_price DECIMAL(10, 2) NULL,
    rating VARCHAR(10) NOT NULL DEFAULT '0.0',
    image VARCHAR(500) NOT NULL DEFAULT '',
    category_id INT NOT NULL,
    sku VARCHAR(80) NOT NULL DEFAULT '',
    cost_price DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    stock_quantity INT NOT NULL DEFAULT 0,
    reorder_level INT NOT NULL DEFAULT 5,
    status VARCHAR(20) NOT NULL DEFAULT 'Out of Stock',
    CONSTRAINT fk_products_category
        FOREIGN KEY (category_id) REFERENCES categories (id)
        ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS restaurant_tables (
    id INT AUTO_INCREMENT PRIMARY KEY,
    table_number INT NOT NULL UNIQUE,
    seats INT NOT NULL DEFAULT 2,
    status VARCHAR(20) NOT NULL DEFAULT 'available',
    zone VARCHAR(40) NOT NULL DEFAULT 'Main Dining',
    shape VARCHAR(20) NOT NULL DEFAULT 'square',
    bg_image VARCHAR(500) NOT NULL DEFAULT '',
    CONSTRAINT chk_table_seats CHECK (seats > 0),
    CONSTRAINT chk_table_status CHECK (status IN ('available', 'occupied', 'reserved'))
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    total_price DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    status VARCHAR(50) NOT NULL DEFAULT 'pending',
    order_type VARCHAR(20) NOT NULL DEFAULT 'dine-in',
    payment_method VARCHAR(20) NOT NULL DEFAULT 'cash',
    delivery_fee DECIMAL(10, 2) NOT NULL DEFAULT 0.00,
    notes TEXT NULL,
    customer_name VARCHAR(160) NULL,
    customer_email VARCHAR(120) NULL,
    customer_phone VARCHAR(40) NULL,
    table_number VARCHAR(20) NULL,
    delivery_address VARCHAR(255) NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_orders_user
        FOREIGN KEY (user_id) REFERENCES users (id)
        ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS order_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    product_id INT NULL,
    quantity INT NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    product_name VARCHAR(120) NOT NULL DEFAULT '',
    product_image VARCHAR(500) NOT NULL DEFAULT '',
    CONSTRAINT chk_order_item_quantity CHECK (quantity > 0),
    CONSTRAINT fk_order_items_order
        FOREIGN KEY (order_id) REFERENCES orders (id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_order_items_product
        FOREIGN KEY (product_id) REFERENCES products (id)
        ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS reservations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    table_id INT NOT NULL,
    reserved_for DATETIME NOT NULL,
    guests INT NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'pending',
    notes TEXT,
    guest_name VARCHAR(160),
    guest_email VARCHAR(120),
    guest_phone VARCHAR(40),
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT chk_reservation_guests CHECK (guests > 0),
    CONSTRAINT fk_reservations_user
        FOREIGN KEY (user_id) REFERENCES users (id)
        ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT fk_reservations_table
        FOREIGN KEY (table_id) REFERENCES restaurant_tables (id)
        ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE=InnoDB;

CREATE TABLE IF NOT EXISTS contact_details (
    id INT AUTO_INCREMENT PRIMARY KEY,
    label VARCHAR(80) NOT NULL,
    details VARCHAR(255) NOT NULL,
    contact VARCHAR(255) NOT NULL,
    contact_url VARCHAR(500),
    sort_order INT NOT NULL DEFAULT 0
) ENGINE=InnoDB;

INSERT IGNORE INTO categories (name) VALUES
    ('Starters'),
    ('Main Course'),
    ('Desserts'),
    ('Beverages'),
    ('Pizza');

INSERT IGNORE INTO restaurant_tables (table_number, seats) VALUES
    (1, 2),
    (2, 2),
    (3, 4),
    (4, 4),
    (5, 6),
    (6, 8);

INSERT INTO contact_details
    (label, details, contact, contact_url, sort_order)
SELECT * FROM (
    SELECT 'Reservations', 'Recommended for dinner and weekend visits',
        '+1 234 567 8900', 'tel:+12345678900', 1
    UNION ALL
    SELECT 'General inquiries', 'Menu questions, dietary needs, and feedback',
        'hello@flavoria.com', 'mailto:hello@flavoria.com', 2
    UNION ALL
    SELECT 'Private events', 'Intimate dinners, weddings, and corporate celebrations',
        'events@flavoria.com', 'mailto:events@flavoria.com', 3
    UNION ALL
    SELECT 'Location', '123 Culinary Avenue, Gourmet District',
        'New York, NY 10001, USA', NULL, 4
    UNION ALL
    SELECT 'Parking', 'Valet service available after 5:00 PM',
        'Street parking nearby', NULL, 5
    UNION ALL
    SELECT 'Dress code', 'Smart casual',
        'Jackets welcome, never required', NULL, 6
) AS seed
WHERE NOT EXISTS (SELECT 1 FROM contact_details);