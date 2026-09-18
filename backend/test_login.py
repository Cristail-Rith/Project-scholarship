
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.chdir(os.path.dirname(os.path.abspath(__file__)))

from app import create_app
app = create_app()

with app.test_client() as client:
    # Try login with new admin account
    resp = client.post('/login', json={
        'email': 'admin@flavoria.com',
        'password': 'admin123'
    })
    print(f'Login (admin@flavoria.com): {resp.status_code}')
    if resp.status_code == 200:
        data = resp.get_json()
        print(f'  Message: {data.get("message")}')
        print(f'  User role: {data.get("user", {}).get("role")}')
        print(f'  Token received: {bool(data.get("access_token"))}')

    # Try login with username
    resp = client.post('/login', json={
        'email': 'admin',
        'password': 'admin123'
    })
    print(f'Login (admin as email): {resp.status_code}')

    # Check all users
    from app.models.user import User
    with app.app_context():
        users = User.query.all()
        print(f'\nTotal users: {len(users)}')
        for u in users:
            print(f'  - {u.username} ({u.email}) role={u.role}')

    # Check products
    from app.models.product import Product
    with app.app_context():
        products = Product.query.all()
        print(f'\nTotal products: {len(products)}')
        for p in products:
            print(f'  - {p.name} (${p.price})')

    # Check categories
    from app.models.category import Category
    with app.app_context():
        cats = Category.query.all()
        print(f'\nTotal categories: {len(cats)}')
        for c in cats:
            print(f'  - {c.name} (slug={c.slug})')

    print('\nAll checks passed!')
