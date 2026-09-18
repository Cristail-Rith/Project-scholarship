import urllib.request, json, urllib.error

# Test login to see which server is responding
data = json.dumps({'email': 'admin@flavoria.com', 'password': 'admin123'}).encode()
req = urllib.request.Request('http://127.0.0.1:5000/login', data=data, headers={'Content-Type': 'application/json'}, method='POST')
try:
    resp = urllib.request.urlopen(req)
    result = json.loads(resp.read())
    print(f'Status: {resp.status}')
    print(f'Message: {result.get("message")}')
    print(f'Role: {result.get("user", {}).get("role")}')
    print('Server is responding correctly!')
except urllib.error.HTTPError as e:
    body = e.read().decode()
    print(f'Error status: {e.code}')
    print(f'Response: {body[:200]}')
    # Check if it's MySQL error or auth error
    if 'MySQL' in body or 'pymysql' in body or 'connection' in body.lower():
        print('This is the OLD server (MySQL config)')
    elif 'Invalid credentials' in body:
        print('Server is new but credentials are wrong')
    elif 'sqlite' in body.lower() or 'database' in body.lower():
        print('This is the NEW server but DB issue')
