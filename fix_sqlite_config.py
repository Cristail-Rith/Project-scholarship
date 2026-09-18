import os

for entry in os.scandir('C:\\Users\\aDMIN'):
    if 'OneDrive' in entry.name:
        test = os.path.join(entry.path, 'Desktop', 'restaurant', 'Project-scholarship', 'frontend', 'app', 'pages', 'orders.vue')
        if os.path.exists(test):
            root = os.path.join(entry.path, 'Desktop', 'restaurant', 'Project-scholarship')
            break

# === 1. Create .env file with SQLite config ===
env_path = os.path.join(root, 'backend', '.env')
env_content = """# Use SQLite for local development (no MySQL server required)
DATABASE_URL=sqlite:///instance/restaurant.db

SECRET_KEY=dev-secret-key-change-me
JWT_SECRET_KEY=jwt-secret-key-change-me
"""
with open(env_path, 'w', encoding='utf-8') as f:
    f.write(env_content)
print(f'.env created at: {env_path}')

# === 2. Fix __init__.py migration to handle SQLite ===
p = os.path.join(root, 'backend', 'app', '__init__.py')
with open(p, 'r', encoding='utf-8') as f:
    c = f.read()

# Replace the migration function with one that handles both MySQL and SQLite
old_migration = """def ensure_order_item_product_id_nullable():
    existing_columns = {
        column["name"]
        for column in inspect(db.engine).get_columns("order_items")
    }
    if "product_id" in existing_columns:
        nullable = inspect(db.engine).get_columns("order_items")
        for col in nullable:
            if col["name"] == "product_id" and col.get("nullable", False):
                return
        db.session.execute(
            text("ALTER TABLE order_items MODIFY COLUMN product_id INT NULL")
        )
        db.session.commit()"""

new_migration = """def ensure_order_item_product_id_nullable():
    existing_columns = {
        column["name"]
        for column in inspect(db.engine).get_columns("order_items")
    }
    if "product_id" not in existing_columns:
        return
    cols = inspect(db.engine).get_columns("order_items")
    for col in cols:
        if col["name"] == "product_id" and col.get("nullable", False):
            return
    dialect = db.engine.dialect.name
    if dialect == "postgresql":
        db.session.execute(text("ALTER TABLE order_items ALTER COLUMN product_id DROP NOT NULL"))
    elif dialect == "mysql":
        db.session.execute(text("ALTER TABLE order_items MODIFY COLUMN product_id INT NULL"))
    elif dialect == "sqlite":
        db.session.execute(text("CREATE TABLE _order_items_new AS SELECT * FROM order_items"))
        db.session.execute(text("DROP TABLE order_items"))
        db.session.execute(text("CREATE TABLE order_items AS SELECT * FROM _order_items_new"))
        db.session.execute(text("DROP TABLE _order_items_new"))
    db.session.commit()"""

c = c.replace(old_migration, new_migration)

with open(p, 'w', encoding='utf-8') as f:
    f.write(c)
print('__init__.py: migration updated for cross-database compatibility')

# Verify
p = os.path.join(root, 'backend', 'app', '__init__.py')
with open(p, 'r', encoding='utf-8') as f:
    c = f.read()
print('\nVerification:')
print('Migration handles sqlite:', 'sqlite' in c and '_order_items_new' in c)
print('Migration handles mysql:', 'mysql' in c and 'MODIFY COLUMN product_id INT NULL' in c)
print('Migration handles postgresql:', 'postgresql' in c and 'DROP NOT NULL' in c)
print('.env exists:', os.path.exists(env_path))

# Verify .env content
with open(env_path, 'r') as f:
    env = f.read()
print('\n.env content:')
print(env)
