#!/usr/bin/env python3
"""
Test authentication backend functionality
"""

import sys
import os

# Add Frappe to path
sys.path.insert(0, '/workspace/development/frappe-bench/apps/frappe')
sys.path.insert(0, '/workspace/development/frappe-bench/apps/lodgeick')

os.chdir('/workspace/development/frappe-bench')
os.environ['FRAPPE_SITE'] = 'lodgeick.com'

import frappe
from frappe.core.doctype.user.user import sign_up

# Initialize Frappe
frappe.init(site='lodgeick.com')
frappe.connect()

print("🧪 Testing Backend Authentication\n")
print("="*60)

# Test 1: Check if signup API is accessible
print("\n1️⃣  Testing signup functionality...")
test_email = f"backend_test_{frappe.utils.now_datetime().strftime('%Y%m%d%H%M%S')}@lodgeick.com"

try:
    result = sign_up(test_email, 'Backend Test User', '/frontend')
    print(f"   ✅ Signup returned: {result}")
except Exception as e:
    print(f"   ⚠️  Signup error: {e}")

# Test 2: Check if user was created
print("\n2️⃣  Checking if user exists...")
if frappe.db.exists('User', test_email):
    user = frappe.get_doc('User', test_email)
    print(f"   ✅ User {test_email} created successfully")
    print(f"   📧 Email: {user.email}")
    print(f"   👤 Name: {user.full_name}")
    print(f"   ✔️  Enabled: {user.enabled}")
else:
    print(f"   ❌ User {test_email} not found in database")

# Test 3: Test login
print("\n3️⃣  Testing login with Administrator...")
from frappe.auth import LoginManager

try:
    login_manager = LoginManager()
    login_manager.authenticate(user='Administrator', pwd='admin')
    login_manager.post_login()
    print(f"   ✅ Login successful as: {frappe.session.user}")
except Exception as e:
    print(f"   ❌ Login error: {e}")

# Test 4: Check session management
print("\n4️⃣  Checking session management...")
try:
    from lodgeick.api.session import get_current_user
    user_info = get_current_user()
    print(f"   ✅ Current user info: {user_info}")
except Exception as e:
    print(f"   ⚠️  Session error: {e}")

print("\n" + "="*60)
print("✅ Backend authentication tests completed!")
print("="*60)

frappe.destroy()
