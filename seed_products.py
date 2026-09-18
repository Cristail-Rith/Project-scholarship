import os, sqlite3

DB_PATH = 'backend/instance/restaurant.db'

# Map the user's category_id (1-indexed from their JSON) to actual DB category IDs
CATEGORY_MAP_BY_NAME = {
    "Grilled Steaks": None,
    "Classic Pizzas": None,
    "Signature Cocktails": None,
    "Decadent Desserts": None,
    "Seasonal Specials": None,
    "Craft Beers": None,
    "BBQ Skewers": None,
    "Cold Salads": None,
}

products = [
    {
        "id": 1,
        "sku": "GRL-001",
        "name": "Ribeye Steak 300g",
        "category": "Grilled Steaks",
        "category_id": 1,
        "description": "Premium ribeye grilled to your preferred doneness, served with garlic butter",
        "image": "/images/products/ribeye-steak.jpg",
        "price": 18.5,
        "previousPrice": 20.0,
        "costPrice": 9.5,
        "sellingPrice": 18.5,
        "stockQuantity": 24,
        "reorderLevel": 10,
        "status": "In Stock",
        "updatedAt": "2026-09-15T09:30:00Z"
    },
    {
        "id": 2,
        "sku": "GRL-002",
        "name": "BBQ Chicken Skewers",
        "category": "BBQ Skewers",
        "category_id": 7,
        "description": "Charcoal-grilled chicken skewers marinated in house BBQ sauce",
        "image": "/images/products/bbq-chicken-skewers.jpg",
        "price": 8.0,
        "previousPrice": None,
        "costPrice": 3.2,
        "sellingPrice": 8.0,
        "stockQuantity": 6,
        "reorderLevel": 15,
        "status": "Low Stock",
        "updatedAt": "2026-09-16T14:10:00Z"
    },
    {
        "id": 3,
        "sku": "PZA-001",
        "name": "Margherita Pizza",
        "category": "Classic Pizzas",
        "category_id": 2,
        "description": "Wood-fired pizza with tomato, mozzarella, and fresh basil",
        "image": "/images/products/margherita-pizza.jpg",
        "price": 11.0,
        "previousPrice": None,
        "costPrice": 4.0,
        "sellingPrice": 11.0,
        "stockQuantity": 40,
        "reorderLevel": 10,
        "status": "In Stock",
        "updatedAt": "2026-09-14T11:00:00Z"
    },
    {
        "id": 4,
        "sku": "PZA-002",
        "name": "Pepperoni Pizza",
        "category": "Classic Pizzas",
        "category_id": 2,
        "description": "Classic pepperoni pizza with mozzarella and house tomato sauce",
        "image": "/images/products/pepperoni-pizza.jpg",
        "price": 12.5,
        "previousPrice": 13.5,
        "costPrice": 4.8,
        "sellingPrice": 12.5,
        "stockQuantity": 0,
        "reorderLevel": 10,
        "status": "Out of Stock",
        "updatedAt": "2026-09-17T08:45:00Z"
    },
    {
        "id": 5,
        "sku": "BAR-001",
        "name": "Old Fashioned Cocktail",
        "category": "Signature Cocktails",
        "category_id": 3,
        "description": "Bourbon, sugar, and bitters, garnished with orange peel",
        "image": "/images/products/old-fashioned.jpg",
        "price": 9.5,
        "previousPrice": None,
        "costPrice": 3.0,
        "sellingPrice": 9.5,
        "stockQuantity": 50,
        "reorderLevel": 20,
        "status": "In Stock",
        "updatedAt": "2026-09-13T18:20:00Z"
    },
    {
        "id": 6,
        "sku": "BAR-002",
        "name": "Mojito",
        "category": "Signature Cocktails",
        "category_id": 3,
        "description": "White rum, lime, mint, and soda water",
        "image": "/images/products/mojito.jpg",
        "price": 8.5,
        "previousPrice": None,
        "costPrice": 2.5,
        "sellingPrice": 8.5,
        "stockQuantity": 12,
        "reorderLevel": 15,
        "status": "Low Stock",
        "updatedAt": "2026-09-16T20:05:00Z"
    },
    {
        "id": 7,
        "sku": "BAR-003",
        "name": "Craft IPA Beer",
        "category": "Craft Beers",
        "category_id": 6,
        "description": "Local craft IPA, 500ml bottle",
        "image": "/images/products/craft-ipa.jpg",
        "price": 6.0,
        "previousPrice": 6.5,
        "costPrice": 2.2,
        "sellingPrice": 6.0,
        "stockQuantity": 80,
        "reorderLevel": 20,
        "status": "In Stock",
        "updatedAt": "2026-09-12T10:15:00Z"
    },
    {
        "id": 8,
        "sku": "PST-001",
        "name": "Chocolate Lava Cake",
        "category": "Decadent Desserts",
        "category_id": 4,
        "description": "Warm chocolate cake with a molten center, served with vanilla ice cream",
        "image": "/images/products/chocolate-lava-cake.jpg",
        "price": 7.5,
        "previousPrice": None,
        "costPrice": 2.8,
        "sellingPrice": 7.5,
        "stockQuantity": 18,
        "reorderLevel": 10,
        "status": "In Stock",
        "updatedAt": "2026-09-15T16:40:00Z"
    },
    {
        "id": 9,
        "sku": "PST-002",
        "name": "New York Cheesecake",
        "category": "Decadent Desserts",
        "category_id": 4,
        "description": "Classic baked cheesecake with a graham cracker crust",
        "image": "/images/products/ny-cheesecake.jpg",
        "price": 6.5,
        "previousPrice": 7.0,
        "costPrice": 2.3,
        "sellingPrice": 6.5,
        "stockQuantity": 5,
        "reorderLevel": 8,
        "status": "Low Stock",
        "updatedAt": "2026-09-17T07:20:00Z"
    },
    {
        "id": 10,
        "sku": "COL-001",
        "name": "Caesar Salad",
        "category": "Cold Salads",
        "category_id": 8,
        "description": "Romaine lettuce, parmesan, croutons, and Caesar dressing",
        "image": "/images/products/caesar-salad.jpg",
        "price": 6.0,
        "previousPrice": None,
        "costPrice": 2.0,
        "sellingPrice": 6.0,
        "stockQuantity": 30,
        "reorderLevel": 10,
        "status": "In Stock",
        "updatedAt": "2026-09-14T09:00:00Z"
    },
    {
        "id": 11,
        "sku": "COL-002",
        "name": "Greek Salad",
        "category": "Cold Salads",
        "category_id": 8,
        "description": "Tomato, cucumber, olives, feta cheese, and olive oil dressing",
        "image": "/images/products/greek-salad.jpg",
        "price": 6.5,
        "previousPrice": None,
        "costPrice": 2.2,
        "sellingPrice": 6.5,
        "stockQuantity": 0,
        "reorderLevel": 10,
        "status": "Out of Stock",
        "updatedAt": "2026-09-16T13:30:00Z"
    },
    {
        "id": 12,
        "sku": "MAIN-001",
        "name": "Truffle Risotto",
        "category": "Seasonal Specials",
        "category_id": 5,
        "description": "Creamy risotto with black truffle shavings and parmesan",
        "image": "/images/products/truffle-risotto.jpg",
        "price": 15.0,
        "previousPrice": None,
        "costPrice": 6.5,
        "sellingPrice": 15.0,
        "stockQuantity": 10,
        "reorderLevel": 5,
        "status": "In Stock",
        "updatedAt": "2026-09-11T12:00:00Z"
    },
    {
        "id": 13,
        "sku": "GRL-003",
        "name": "Grilled Salmon Fillet",
        "category": "Grilled Steaks",
        "category_id": 1,
        "description": "Fresh salmon fillet grilled with lemon butter sauce",
        "image": "/images/products/grilled-salmon.jpg",
        "price": 16.0,
        "previousPrice": 17.5,
        "costPrice": 7.0,
        "sellingPrice": 16.0,
        "stockQuantity": 14,
        "reorderLevel": 10,
        "status": "In Stock",
        "updatedAt": "2026-09-15T15:00:00Z"
    },
    {
        "id": 14,
        "sku": "PZA-003",
        "name": "Quattro Formaggi Pizza",
        "category": "Classic Pizzas",
        "category_id": 2,
        "description": "Four-cheese pizza with mozzarella, gorgonzola, parmesan, and provolone",
        "image": "/images/products/quattro-formaggi.jpg",
        "price": 13.0,
        "previousPrice": None,
        "costPrice": 5.0,
        "sellingPrice": 13.0,
        "stockQuantity": 8,
        "reorderLevel": 10,
        "status": "Low Stock",
        "updatedAt": "2026-09-17T06:15:00Z"
    },
    {
        "id": 15,
        "sku": "PST-003",
        "name": "Discontinued Tiramisu Cups",
        "category": "Decadent Desserts",
        "category_id": 4,
        "description": "Individual tiramisu cups, previously offered as a seasonal item",
        "image": "/images/products/tiramisu-cups.jpg",
        "price": 5.5,
        "previousPrice": 5.5,
        "costPrice": 2.0,
        "sellingPrice": 5.5,
        "stockQuantity": 0,
        "reorderLevel": 0,
        "status": "Archived",
        "updatedAt": "2026-08-30T10:00:00Z"
    }
]

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Build category name -> ID map from the database
cursor.execute("SELECT id, name FROM categories")
for cat_id, cat_name in cursor.fetchall():
    if cat_name in CATEGORY_MAP_BY_NAME:
        CATEGORY_MAP_BY_NAME[cat_name] = cat_id

print("Category name -> DB ID mapping:")
for name, db_id in CATEGORY_MAP_BY_NAME.items():
    print(f"  {name} -> {db_id}")

# Check existing products by SKU
cursor.execute("SELECT sku FROM products")
existing_skus = {row[0] for row in cursor.fetchall()}
print(f"\nExisting SKUs: {existing_skus}")

inserted = 0
for prod in products:
    if prod['sku'] in existing_skus:
        print(f"  SKIP (already exists): {prod['sku']} - {prod['name']}")
        continue
    
    cat_db_id = CATEGORY_MAP_BY_NAME.get(prod['category'])
    if cat_db_id is None:
        print(f"  SKIP (category not found): {prod['category']}")
        continue
    
    cursor.execute("""
        INSERT INTO products (name, description, price, previous_price, rating, image, category_id, sku, cost_price, stock_quantity, reorder_level, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        prod['name'],
        prod['description'],
        prod['price'],
        prod.get('previousPrice'),
        '0.0',
        prod['image'],
        cat_db_id,
        prod['sku'],
        prod['costPrice'],
        prod['stockQuantity'],
        prod['reorderLevel'],
        prod['status']
    ))
    print(f"  INSERTED: {prod['sku']} - {prod['name']} (category_id={cat_db_id})")
    inserted += 1

conn.commit()

# Verify
cursor.execute("""
    SELECT p.id, p.name, p.sku, p.price, p.status, p.stock_quantity, c.name as cat_name
    FROM products p 
    JOIN categories c ON p.category_id = c.id 
    ORDER BY p.id
""")
print(f"\n=== All {cursor.execute('SELECT COUNT(*) FROM products').fetchone()[0]} products in DB ===")
for row in cursor.fetchall():
    print(f"  ID={row[0]} | {row[1]:35s} | SKU={row[2]:10s} | price={row[3]:>5.2f} | status={row[4]:12s} | stock={row[5]:>3} | cat={row[6]}")

conn.close()
print(f"\nDone! Inserted {inserted} new products.")
