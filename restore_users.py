import os, sqlite3, shutil

root = None
for entry in os.scandir('C:\\Users\\aDMIN'):
    if 'OneDrive' in entry.name:
        test = os.path.join(entry.path, 'Desktop', 'restaurant', 'Project-scholarship')
        if os.path.exists(os.path.join(test, 'backend', 'app', 'config.py')):
            root = test
            break

db_path = os.path.join(root, 'backend', 'instance', 'restaurant.db')
bak_path = os.path.join(root, 'backend', 'instance', 'restaurant.db.bak')

print('Current DB exists:', os.path.exists(db_path))
print('Backup DB exists:', os.path.exists(bak_path))

if os.path.exists(bak_path):
    # Extract users from the backup
    try:
        conn_bak = sqlite3.connect(bak_path)
        cursor = conn_bak.cursor()
        
        # Check what tables exist in backup
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [t[0] for t in cursor.fetchall()]
        print('Tables in backup:', tables)
        
        # Get users from backup
        if 'users' in tables:
            cursor.execute("SELECT id, username, email, phone, password_hash, avatar, role FROM users")
            users = cursor.fetchall()
            print(f'Users in backup: {len(users)}')
            for u in users:
                print(f'  - id={u[0]}, username={u[1]}, email={u[2]}, role={u[6]}')
        
        conn_bak.close()
        
        # Now insert users into the new DB
        conn_new = sqlite3.connect(db_path)
        cursor_new = conn_new.cursor()
        
        # Check if users already exist in new DB
        cursor_new.execute("SELECT COUNT(*) FROM users")
        existing_count = cursor_new.fetchone()[0]
        print(f'Users in new DB: {existing_count}')
        
        if existing_count == 0 and len(users) > 0:
            # Copy users from backup
            conn_bak = sqlite3.connect(bak_path)
            cursor_bak = conn_bak.cursor()
            cursor_bak.execute("SELECT id, username, email, phone, password_hash, avatar, role FROM users")
            
            for user in cursor_bak.fetchall():
                try:
                    cursor_new.execute(
                        "INSERT OR REPLACE INTO users (id, username, email, phone, password_hash, avatar, role) VALUES (?, ?, ?, ?, ?, ?, ?)",
                        user
                    )
                    print(f'  Restored user: {user[1]} ({user[2]}) - role={user[6]}')
                except Exception as e:
                    print(f'  Error restoring user {user[1]}: {e}')
            
            conn_bak.close()
            conn_new.commit()
            print('Users restored successfully!')
        
        conn_new.close()
        
        # Also restore products and categories
        conn_bak = sqlite3.connect(bak_path)
        conn_new = sqlite3.connect(db_path)
        
        # Check products
        cursor_bak = conn_bak.cursor()
        cursor_bak.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='products'")
        if cursor_bak.fetchone():
            cursor_bak.execute("SELECT * FROM products")
            products = cursor_bak.fetchall()
            print(f'\nProducts in backup: {len(products)}')
            
            # Get column names
            cursor_bak.execute("PRAGMA table_info(products)")
            cols = [c[1] for c in cursor_bak.fetchall()]
            
            cursor_new = conn_new.cursor()
            for product in products:
                try:
                    placeholders = ', '.join(['?' for _ in product])
                    cursor_new.execute(
                        f"INSERT OR REPLACE INTO products ({', '.join(cols)}) VALUES ({placeholders})",
                        product
                    )
                except Exception as e:
                    print(f'  Error restoring product: {e}')
            conn_new.commit()
            print(f'Products restored!')
        
        # Check categories
        cursor_bak.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='categories'")
        if cursor_bak.fetchone():
            cursor_bak.execute("SELECT * FROM categories")
            categories = cursor_bak.fetchall()
            print(f'\nCategories in backup: {len(categories)}')
            
            cursor_bak.execute("PRAGMA table_info(categories)")
            cols = [c[1] for c in cursor_bak.fetchall()]
            
            cursor_new = conn_new.cursor()
            for cat in categories:
                try:
                    placeholders = ', '.join(['?' for _ in cat])
                    cursor_new.execute(
                        f"INSERT OR REPLACE INTO categories ({', '.join(cols)}) VALUES ({placeholders})",
                        cat
                    )
                except Exception as e:
                    print(f'  Error restoring category: {e}')
            conn_new.commit()
            print(f'Categories restored!')
        
        # Check tables (restaurant tables)
        cursor_bak.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='tables'")
        if cursor_bak.fetchone():
            cursor_bak.execute("SELECT * FROM tables")
            tables_data = cursor_bak.fetchall()
            print(f'\nTables in backup: {len(tables_data)}')
            
            cursor_bak.execute("PRAGMA table_info(tables)")
            cols = [c[1] for c in cursor_bak.fetchall()]
            
            cursor_new = conn_new.cursor()
            for t in tables_data:
                try:
                    placeholders = ', '.join(['?' for _ in t])
                    cursor_new.execute(
                        f"INSERT OR REPLACE INTO tables ({', '.join(cols)}) VALUES ({placeholders})",
                        t
                    )
                except Exception as e:
                    print(f'  Error restoring table: {e}')
            conn_new.commit()
            print(f'Tables restored!')
        
        conn_bak.close()
        conn_new.close()
        print('\nAll data restored from backup!')
        
    except Exception as e:
        print(f'Error: {e}')
else:
    print('No backup found - creating default admin user')
    
    # Create a default admin user
    from werkzeug.security import generate_password_hash
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Check if admin exists
    cursor.execute("SELECT * FROM users WHERE username = 'admin'")
    if cursor.fetchone():
        print('Admin user already exists')
    else:
        cursor.execute(
            "INSERT INTO users (username, email, phone, password_hash, avatar, role) VALUES (?, ?, ?, ?, ?, ?)",
            ('admin', 'admin@flavoria.com', '', generate_password_hash('admin123'), '', 'admin')
        )
        conn.commit()
        print('Default admin user created: admin / admin123')
    
    conn.close()
