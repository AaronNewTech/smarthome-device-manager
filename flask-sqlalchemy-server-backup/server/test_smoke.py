from app import create_app

app = create_app()

with app.app_context():
    client = app.test_client()
    r1 = client.get('/api/rooms')
    print('GET /api/rooms ->', r1.status_code)
    print(r1.get_json())

    r2 = client.get('/api/devices')
    print('GET /api/devices ->', r2.status_code)
    print(r2.get_json())

    r3 = client.get('/api/stats')
    print('GET /api/stats ->', r3.status_code)
    print(r3.get_json())
