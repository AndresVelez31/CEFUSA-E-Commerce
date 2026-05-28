import urllib.request, json

body = b'{"amount": 120000, "discount_code": "SAVE10"}'
req = urllib.request.Request(
    'http://localhost/api/v2/checkout/',
    data=body,
    headers={'Content-Type': 'application/json'}
)
r = urllib.request.urlopen(req)
print('NGINX->FLASK OK:', json.loads(r.read()))
