import os
import mysql.connector
from dotenv import load_dotenv

# Load .env file
load_dotenv()

# Read DB configuration directly from .env - NO settings.py layer
DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_DATABASE"),
    "port": int(os.getenv("DB_PORT", 3306)),
    "ssl_disabled": os.getenv("DB_SSL_DISABLED", "True").lower() == "true",
}

def get_db_connection():
    """Create and return database connection"""
    try:
        conn = mysql.connector.connect(
            host=DB_CONFIG["host"],
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"],
            database=DB_CONFIG["database"],
            port=DB_CONFIG["port"]
        )
        return conn
    except Exception as e:
        print(f"Error creating database connection: {e}")
        return None

def user_exists(email):
    """Check if user exists in vendor table"""
    try:
        conn = get_db_connection()
        if not conn:
            return False
        cur = conn.cursor()
        cur.execute("SELECT email FROM vendor WHERE email=%s", (email,))
        result = cur.fetchone()
        cur.close()
        conn.close()
        return result is not None
    except Exception as e:
        print(f"Error checking user: {e}")
        return False

def update_mobile_verified(email):
    """Update mobile_verified status to 1 for a vendor"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("UPDATE vendor SET mobile_verified = 1 WHERE email=%s", (email,))
        conn.commit()
        cur.close()
        conn.close()
        print(f"Updated mobile_verified for {email}")
        return True
    except Exception as e:
        print(f"Error updating mobile_verified: {e}")
        return False

def delete_vendor(email):
    """Delete vendor by email (for cleanup)"""
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM vendor WHERE email=%s", (email,))
        conn.commit()
        cur.close()
        conn.close()
        return True
    except Exception as e:
        print(f"Error deleting vendor: {e}")
        return False
