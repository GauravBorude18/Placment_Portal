import os, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'placement_core.settings')
django.setup()
from django.test import Client

c = Client()

# 1. Test PIN code lookups
pincodes_to_test = ['411001', '400001', '414001', '110001', '560001', '422001']
for pin in pincodes_to_test:
    resp = c.get(f'/api/pincode-lookup/{pin}/')
    print(f'Lookup {pin} Status: {resp.status_code}', resp.json())
    assert resp.status_code == 200
    assert resp.json()['success'] == True

# 2. Test Invalid PIN code
resp_inv = c.get('/api/pincode-lookup/123/')
print('Invalid PIN lookup status:', resp_inv.status_code)
assert resp_inv.status_code == 400

# 3. Test Registration Validation (Invalid Phone)
resp_reg_inv = c.post('/register/', {
    'username': 'testuser999',
    'roll_number': '99999999',
    'full_name': 'Test Candidate',
    'email': 'test999@a2z.edu',
    'password': 'password123',
    'confirm_password': 'password123',
    'phone_number': '123', # Invalid phone length
    'permanent_address': 'Flat 101, Test Road',
    'city': 'Pune',
    'state': 'Maharashtra',
    'pincode': '411001',
    'cgpa': '8.50',
    'tenth_percentage': '92.00',
    'twelfth_percentage': '94.00'
})
assert b'Primary Mobile Number must be exactly 10 digits' in resp_reg_inv.content
print('Verified: Invalid phone blocked during registration!')

# 4. Test Registration Validation (Invalid CGPA)
resp_reg_cgpa = c.post('/register/', {
    'username': 'testuser999',
    'roll_number': '99999999',
    'full_name': 'Test Candidate',
    'email': 'test999@a2z.edu',
    'password': 'password123',
    'confirm_password': 'password123',
    'phone_number': '9822012345',
    'permanent_address': 'Flat 101, Test Road',
    'city': 'Pune',
    'state': 'Maharashtra',
    'pincode': '411001',
    'cgpa': '15.50', # Invalid CGPA > 10
    'tenth_percentage': '92.00',
    'twelfth_percentage': '94.00'
})
assert b'valid CPI / CGPA between 0.0 and 10.0' in resp_reg_cgpa.content
print('Verified: Invalid CGPA blocked during registration!')

# 5. Test Registration Validation (Invalid PIN Code)
resp_reg_pin = c.post('/register/', {
    'username': 'testuser999',
    'roll_number': '99999999',
    'full_name': 'Test Candidate',
    'email': 'test999@a2z.edu',
    'password': 'password123',
    'confirm_password': 'password123',
    'phone_number': '9822012345',
    'permanent_address': 'Flat 101, Test Road',
    'city': 'Pune',
    'state': 'Maharashtra',
    'pincode': '411', # Invalid PIN Code < 6
    'cgpa': '8.50',
    'tenth_percentage': '92.00',
    'twelfth_percentage': '94.00'
})
assert b'PIN Code must be exactly 6 digits' in resp_reg_pin.content
print('Verified: Invalid PIN code blocked during registration!')

print('ALL VALIDATION & PINCODE LOOKUP TESTS PASSED 100%!')
