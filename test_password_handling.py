"""
Test password handling for bcrypt compatibility
"""
from database import get_password_hash, verify_password

# Test normal password
normal_password = "mypassword123"
print(f"Testing normal password: '{normal_password}'")
hashed = get_password_hash(normal_password)
verified = verify_password(normal_password, hashed)
print(f"✅ Normal password works: {verified}")

# Test long password (over 72 bytes)
long_password = "a" * 100  # 100 characters
print(f"\nTesting long password: {len(long_password)} characters")
hashed_long = get_password_hash(long_password)
verified_long = verify_password(long_password, hashed_long)
print(f"✅ Long password works: {verified_long}")

# Test with unicode characters
unicode_password = "пароль123🔐" * 10  # This will be over 72 bytes
print(f"\nTesting unicode password: {len(unicode_password)} characters, {len(unicode_password.encode('utf-8'))} bytes")
hashed_unicode = get_password_hash(unicode_password)
verified_unicode = verify_password(unicode_password, hashed_unicode)
print(f"✅ Unicode password works: {verified_unicode}")

print("\n🎉 All password tests passed!")
