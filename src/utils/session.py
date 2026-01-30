import os
import time
import random
from dotenv import load_dotenv
from src.utils.db import user_exists

# Load .env file
load_dotenv()

# Read password directly from .env - NO settings.py layer
HARD_PASSWORD = os.getenv("HARD_PASSWORD", "Test@1234")

# Global session storage for E2E test only
_test_session = {
    "user": None,
    "created": False
}

def unique_email():
    """Generate unique email with milliseconds timestamp - truly unique"""
    return f"auto_{int(time.time() * 1000)}_{random.randint(10000, 99999)}@gmail.in"

def unique_mobile():
    """Generate valid 10-digit mobile number starting with 9"""
    return "9" + str(random.randint(100000000, 999999999))

def create_fresh_test_user():
    """
    Create a FRESH test user with unique email and mobile
    For each test case - generates completely new user data
    Does NOT cache or reuse users across tests
    
    This is what most tests should use - each test gets its own user!
    
    Returns:
        dict: User data with first_name, last_name, email, mobile, password, etc.
    """
    # Keep generating new emails until we find one that doesn't exist
    email = None
    max_attempts = 10
    
    for attempt in range(max_attempts):
        email = unique_email()
        if not user_exists(email):
            # Email doesn't exist, use it
            break
        else:
            if attempt < 3:  # Only print first few attempts
                print(f"Email exists, trying another... (attempt {attempt+1}/{max_attempts})")
    
    user = {
        "first_name": "AutoTest",
        "last_name": "User",
        "email": email,
        "mobile": unique_mobile(),
        "password": HARD_PASSWORD,
        "confirm_password": HARD_PASSWORD,
        "referral_code": None,
        "toc": True
    }
    
    return user

def create_test_session():
    """
    Create test user and store in global session
    ONLY used for E2E test that needs persistent user across multiple steps
    
    For individual tests, use create_fresh_test_user() instead!
    
    Returns:
        dict: User data with first_name, last_name, email, mobile, password, etc.
    """
    global _test_session
    
    if _test_session["user"] is None:
        _test_session["user"] = create_fresh_test_user()
        _test_session["created"] = True
        print(f"\n✅ Test session created with email: {_test_session['user']['email']}")
    
    return _test_session["user"]

def get_test_user():
    """Get stored test user from session (for E2E test only)
    
    Returns:
        dict: User data or None if session not created
    """
    global _test_session
    
    if _test_session["user"] is None:
        # Auto-create if not exists
        return create_test_session()
    
    return _test_session["user"]

def get_test_user_email():
    """Get email of test user"""
    user = get_test_user()
    return user["email"] if user else None

def get_test_user_password():
    """Get password of test user"""
    user = get_test_user()
    return user["password"] if user else None

def cleanup_test_session():
    """Clear test session and user data"""
    global _test_session
    _test_session["user"] = None
    _test_session["created"] = False
    print("\n✅ Test session cleaned up")

def is_session_created():
    """Check if test session is already created"""
    return _test_session["created"]

def reset_test_session():
    """Reset session (used between test suites)"""
    cleanup_test_session()
