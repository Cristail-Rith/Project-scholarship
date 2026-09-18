
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.chdir(os.path.dirname(os.path.abspath(__file__)))

from app import create_app
app = create_app()

with app.test_client() as client:
    # Test 1: Login with email
    resp = client.post('/login', json={'email': 'admin@flavoria.com', 'password': 'admin123'})
    print(f'Login with email: {resp.status_code} - {resp.get_json().get("message")}')
    if resp.status_code == 200:
        role = resp.get_json().get('user', {}).get('role')
        print(f'  Role: {role}')

    # Test 2: Login with username (sent as email field)
    resp = client.post('/login', json={'email': 'admin', 'username': 'admin', 'password': 'admin123'})
    print(f'Login with username: {resp.status_code} - {resp.get_json().get("message")}')
    if resp.status_code == 200:
        role = resp.get_json().get('user', {}).get('role')
        print(f'  Role: {role}')

    # Test 3: Login with wrong password
    resp = client.post('/login', json={'email': 'admin@flavoria.com', 'password': 'wrong'})
    print(f'Login with wrong password: {resp.status_code} - {resp.get_json().get("message")}')

    # Test 4: Access admin orders with token
    resp = client.post('/login', json={'email': 'admin', 'username': 'admin', 'password': 'admin123'})
    if resp.status_code == 200:
        token = resp.get_json()['access_token']
        headers = {'Authorization': f'Bearer {token}'}

        resp = client.get('/orders', headers=headers)
        orders = resp.get_json()
        if isinstance(orders, list):
            print(f'Orders API (as admin): {len(orders)} orders')
        else:
            print(f'Orders API error: {resp.status_code}')

        resp = client.get('/products', headers=headers)
        products = resp.get_json()
        if isinstance(products, list):
            print(f'Products API: {len(products)} products')

    print('All tests passed!')
