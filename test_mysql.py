from auth import register_user, login_user
from history import save_history
import random
import string

def random_email():
    return ''.join(random.choices(string.ascii_lowercase, k=10)) + "@test.com"

def test_integration():
    print("--- Testing MySQL Integration ---")
    
    email = random_email()
    password = "password123"
    name = "Test User"
    
    # 1. Test Registration
    print(f"Testing Registration with email: {email}...")
    ok, msg = register_user(name, email, password)
    if ok:
        print("SUCCESS: Registration Successful!")
    else:
        print(f"FAILED: Registration Failed: {msg}")
        return
        
    # 2. Test Login
    print("Testing Login...")
    ok, msg, user_id, user_name = login_user(email, password)
    if ok:
        print(f"SUCCESS: Login Successful! User ID: {user_id}, Name: {user_name}")
    else:
        print(f"FAILED: Login Failed: {msg}")
        return
        
    # 3. Test History Logging
    print("Testing Command History Logging...")
    ok = save_history(user_id, "test command", "test response", input_mode="text")
    if ok:
        print("SUCCESS: History Logging Successful!")
    else:
        print("FAILED: History Logging Failed!")
        
    print("--- Integration Test Complete ---")

if __name__ == "__main__":
    test_integration()
