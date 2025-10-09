#!/usr/bin/env python3
"""
Test the authentication flow for Lodgeick
Tests signup, login, and app connection flows
"""

import time
import random
from playwright.sync_api import sync_playwright, expect

# Test configuration
BASE_URL = "http://home.localhost:8080"  # Frontend URL (per user instructions)
# BASE_URL = "http://localhost:8006"  # Alternative dev server
TEST_EMAIL = f"test{random.randint(1000, 9999)}@lodgeick.com"
TEST_PASSWORD = "Test123!@#"
TEST_NAME = "Test User"

def test_auth_flow():
    """Test the complete authentication flow"""

    with sync_playwright() as p:
        # Launch browser
        browser = p.chromium.launch(headless=False, slow_mo=500)
        context = browser.new_context(viewport={"width": 1280, "height": 720})
        page = context.new_page()

        print(f"\n🚀 Starting authentication flow test...")
        print(f"📧 Test email: {TEST_EMAIL}")
        print(f"🌐 Base URL: {BASE_URL}\n")

        try:
            # Step 1: Visit home page
            print("1️⃣  Visiting home page...")
            page.goto(BASE_URL)
            page.wait_for_load_state("networkidle")

            # Wait for catalog to load
            page.wait_for_selector(".card-app", timeout=10000)
            print("   ✅ Home page loaded successfully")

            # Step 2: Try to connect an app (should show auth modal)
            print("\n2️⃣  Clicking 'Connect App' as guest...")
            app_cards = page.locator(".card-app").all()
            if app_cards:
                app_cards[0].click()
                page.wait_for_selector(".modal-content", timeout=5000)
                print("   ✅ App details modal opened")

                # Click "Connect App" button
                page.locator("button:has-text('Connect App')").click()
                page.wait_for_selector(".modal-content:has-text('Authentication Required')", timeout=5000)
                print("   ✅ Authentication modal appeared")

            # Step 3: Go to signup page
            print("\n3️⃣  Navigating to signup page...")
            page.locator("a:has-text('Create Free Account')").click()
            page.wait_for_url("**/account/signup")
            print("   ✅ Signup page loaded")

            # Step 4: Fill signup form
            print("\n4️⃣  Filling signup form...")
            page.fill("input[type='text']", TEST_NAME)
            page.fill("input[type='email']", TEST_EMAIL)
            page.fill("input[type='password']", TEST_PASSWORD)
            print(f"   ✅ Form filled with: {TEST_NAME} / {TEST_EMAIL}")

            # Step 5: Submit signup
            print("\n5️⃣  Submitting signup form...")
            page.locator("button[type='submit']").click()

            # Wait for either success redirect or error
            time.sleep(2)

            # Check for alerts or redirects
            current_url = page.url
            print(f"   📍 Current URL: {current_url}")

            if "signup" not in current_url:
                print("   ✅ Signup successful - redirected!")
            else:
                # Check for error messages
                error_selector = ".alert-danger"
                if page.locator(error_selector).count() > 0:
                    error_msg = page.locator(error_selector).inner_text()
                    print(f"   ⚠️  Signup error: {error_msg}")
                else:
                    print("   ⚠️  Still on signup page - checking for validation")

            # Step 6: Try to login
            print("\n6️⃣  Navigating to login page...")
            page.goto(f"{BASE_URL}/account/login")
            page.wait_for_load_state("networkidle")
            print("   ✅ Login page loaded")

            # Fill login form
            print("\n7️⃣  Filling login form...")
            page.fill("input[type='email']", "Administrator")
            page.fill("input[type='password']", "admin")
            print("   ✅ Form filled with Administrator credentials")

            # Submit login
            print("\n8️⃣  Submitting login form...")
            page.locator("button[type='submit']").click()
            time.sleep(2)

            current_url = page.url
            print(f"   📍 Current URL after login: {current_url}")

            if "login" not in current_url:
                print("   ✅ Login successful - redirected to home!")

                # Step 7: Check if user is logged in
                print("\n9️⃣  Checking authentication status...")
                page.wait_for_selector(".navbar", timeout=5000)

                # Look for logout button
                if page.locator("button:has-text('Logout')").count() > 0:
                    print("   ✅ User is authenticated (Logout button found)")

                    # Try to connect app again
                    print("\n🔟 Testing app connection as authenticated user...")
                    app_cards = page.locator(".card-app").all()
                    if app_cards:
                        app_cards[0].click()
                        page.wait_for_selector(".modal-content", timeout=5000)

                        # Click connect button
                        page.locator("button:has-text('Connect App')").click()
                        time.sleep(1)

                        # Should not show auth modal anymore
                        if page.locator(".modal-content:has-text('Authentication Required')").count() == 0:
                            print("   ✅ Authentication modal NOT shown - user is authenticated!")
                        else:
                            print("   ⚠️  Authentication modal still appearing")
                else:
                    print("   ⚠️  Logout button not found")
            else:
                error_selector = ".alert-danger"
                if page.locator(error_selector).count() > 0:
                    error_msg = page.locator(error_selector).inner_text()
                    print(f"   ❌ Login error: {error_msg}")
                else:
                    print("   ⚠️  Still on login page")

            print("\n" + "="*60)
            print("✅ TEST COMPLETED")
            print("="*60)

            # Keep browser open for inspection
            input("\nPress Enter to close browser...")

        except Exception as e:
            print(f"\n❌ ERROR: {e}")
            import traceback
            traceback.print_exc()
            input("\nPress Enter to close browser...")

        finally:
            browser.close()

if __name__ == "__main__":
    test_auth_flow()
