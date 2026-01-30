"""
Complete End-to-End Authentication Flow Test
Covers: Signup → Mobile Verification → Logout → Login → Merchant Agreement → Orders

Status: ENABLED
- Signup: ✅ Works
- Mobile Verification Page: ✅ Works  
- Database Update: ✅ Should work now (staging DB configured)
- Login: ✅ Should work now
"""
import pytest
from src.flows.authentication_flow import AuthenticationFlow
from src.utils.db import update_mobile_verified, delete_vendor
from src.utils.session import create_test_session, get_test_user, cleanup_test_session


class TestAuthenticationEToE:
    """End-to-End Authentication Flow Tests"""
    
    def test_01_auth_positive_e2e(self, sb):
        """
        E2E Test: Complete authentication flow
        
        Test User:
        - Email: Auto-generated (auto_[timestamp]_[random]@gmail.in)
        - Mobile: 10-digit auto-generated starting with 9
        - Password: Test@1234
        
        Status: Partially working (stopped at DB update due to permissions)
        """
        # SETUP: Create test user
        print(f"\n{'='*70}")
        print(f"SETUP: Creating Test User")
        print(f"{'='*70}")
        
        user = create_test_session()
        print(f"\n✅ TEST USER CREATED:")
        print(f"   Email: {user['email']}")
        print(f"   Mobile: {user['mobile']}")
        print(f"   Password: {user['password']}")
        
        email = user["email"]
        password = user["password"]
        
        try:
            flow = AuthenticationFlow(sb)
            
            # Step 1: SIGNUP
            print(f"\n{'='*70}")
            print(f"STEP 1: SIGNUP WITH VALID DATA")
            print(f"{'='*70}")
            flow.step_1_signup(user)
            print(f"✅ Step 1 Complete: User signed up")
            
            # Step 2: VERIFY MOBILE PAGE
            print(f"\n{'='*70}")
            print(f"STEP 2: VERIFY MOBILE VERIFICATION PAGE")
            print(f"{'='*70}")
            flow.step_2_wait_and_verify_mobile_page()
            print(f"✅ Step 2 Complete: On mobile verification page")
            
            # Step 3: UPDATE DATABASE
            print(f"\n{'='*70}")
            print(f"STEP 3: UPDATE DATABASE (mobile_verified = 1)")
            print(f"{'='*70}")
            assert update_mobile_verified(email), f"Failed to update mobile_verified for {email}"
            print(f"✅ Step 3 Complete: Database updated")
            
            # Step 4: LOGOUT & LOGIN
            print(f"\n{'='*70}")
            print(f"STEP 4: LOGOUT & NAVIGATE TO LOGIN")
            print(f"{'='*70}")
            flow.step_3_logout_and_navigate_to_login()
            print(f"✅ Step 4 Complete: Logged out")
            
            # Step 5: LOGIN
            print(f"\n{'='*70}")
            print(f"STEP 5: LOGIN WITH CREDENTIALS")
            print(f"{'='*70}")
            flow.step_4_login(email, password)
            print(f"✅ Step 5 Complete: Logged in")
            
            # Step 6: MERCHANT AGREEMENT
            print(f"\n{'='*70}")
            print(f"STEP 6: ACCEPT MERCHANT AGREEMENT")
            print(f"{'='*70}")
            flow.step_5_accept_merchant_agreement()
            print(f"✅ Step 6 Complete: Agreement accepted")
            
            # Step 7: VERIFY ORDERS PAGE
            print(f"\n{'='*70}")
            print(f"STEP 7: NAVIGATE TO ORDERS PAGE")
            print(f"{'='*70}")
            # After accepting merchant agreement, navigate to orders page
            sb.open("https://dev.v.shipgl.in/orders/all")
            sb.wait(3)
            current_url = sb.get_current_url()
            print(f"Current URL: {current_url}")
            assert "orders" in current_url, f"Expected orders page, got {current_url}"
            print(f"✅ Step 7 Complete: On orders page")
            
            # Step 8: NAVIGATE TO LOGOUT URL AND LOGOUT
            print(f"\n{'='*70}")
            print(f"STEP 8: LOGOUT")
            print(f"{'='*70}")
            sb.open("https://dev.v.shipgl.in/logout")
            sb.wait(3)
            print(f"✅ Step 8 Complete: Logout URL accessed")
            
            # Step 9: NAVIGATE TO SIGNUP PAGE FOR NEXT TESTS
            print(f"\n{'='*70}")
            print(f"STEP 9: PREPARE FOR NEXT TESTS")
            print(f"{'='*70}")
            sb.open("https://dev.v.shipgl.in/auth/signup")
            print(f"✅ Step 9 Complete: On signup page, ready for next tests")
            
            print(f"\n{'='*70}")
            print(f"✅ E2E TEST PASSED - FULL FLOW COMPLETED")
            print(f"{'='*70}\n")
            
        finally:
            # TEARDOWN: Clean up (but keep test user in DB to verify mobile_verified=1)
            try:
                print(f"\nTEARDOWN: Cleaning up")
                # NOTE: Commenting out delete so you can verify mobile_verified=1 in database
                # delete_vendor(email)
                cleanup_test_session()
                print(f"✅ Test session cleaned up")
                print(f"ℹ️  Test user KEPT in database: {email}")
                print(f"ℹ️  You can check: SELECT * FROM vendor WHERE email='{email}'")
            except Exception as e:
                print(f"⚠️ Cleanup error: {e}")

