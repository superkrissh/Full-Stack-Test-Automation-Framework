"""
Pytest configuration for authentication tests
Handles browser session management and test setup/teardown
"""
import pytest
from seleniumbase import BaseCase


@pytest.fixture(scope="session")
def sb():
    """
    SeleniumBase browser fixture - SESSION SCOPE
    
    ✅ Browser opens ONCE at session start
    ✅ Browser stays open for ALL tests
    ✅ Browser refreshes between tests (no close/open)
    ✅ All tests share same browser instance
    
    This ensures:
    - Fast test execution (no browser restart overhead)
    - Stable browser state across tests
    - Simple page refresh instead of close/open
    """
    base = BaseCase()
    base.setUp()
    
    # Browser is now open
    print(f"\n{'='*70}")
    print(f"✅ BROWSER OPENED - SESSION SCOPE (ONE TIME)")
    print(f"   Will refresh pages instead of close/open")
    print(f"{'='*70}\n")
    
    yield base
    
    # Cleanup - browser closes
    base.tearDown()
    print(f"\n{'='*70}")
    print(f"✅ BROWSER CLOSED - SESSION COMPLETE")
    print(f"{'='*70}\n")

