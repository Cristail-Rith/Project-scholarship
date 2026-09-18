
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.chdir(os.path.dirname(os.path.abspath(__file__)))

from app import create_app
app = create_app()

with app.test_client() as client:
    # Login with admin
    resp = client.post('/login', json={
        'email': 'admin@flavoria.com',
        'password': 'admin123'
    })
    print(f'Login status: {resp.status_code}')
    data = resp.get_json()
    print(f'Message: {data.get("message")}')
    print(f'User role: {data.get("user", {}).get("role")}')
    print(f'User email: {data.get("user", {}).get("email")}')
    print(f'Token received: {bool(data.get("access_token"))}')

    if resp.status_code == 200:
        token = data['access_token']
        headers = {'Authorization': f'Bearer {token}'}

        # Get orders
        resp = client.get('/orders', headers=headers)
        orders = resp.get_json()
        if isinstance(orders, list):
            print(f'Orders API: returns list of {len(orders)} orders')
        else:
            print(f'Orders API: unexpected format - {type(orders)}')

        # Get products
        resp = client.get('/products', headers=headers)
        products = resp.get_json()
        if isinstance(products, list):
            print(f'Products API: returns list of {len(products)} products')
            for p in products:
                print(f'  - {p.get("name", p.get("title", "N/A"))}: ${p.get("price", "N/A")}')
        else:
            print(f'Products API: {type(products)}')

    print('\nLogin verified!')
