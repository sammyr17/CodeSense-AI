"""
Test bcrypt compatibility fixes
"""
print("Testing bcrypt compatibility...")

# Test 1: Direct bcrypt approach
print("\n1. Testing direct bcrypt approach:")
try:
    import bcrypt
    password = "test12"
    salt = bcrypt.gensalt(rounds=12)
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    verified = bcrypt.checkpw(password.encode('utf-8'), hashed)
    print(f"✅ Direct bcrypt works: {verified}")
except Exception as e:
    print(f"❌ Direct bcrypt failed: {e}")

# Test 2: Fixed database module
print("\n2. Testing fixed database module:")
try:
    from database_fixed import get_password_hash, verify_password
    password = "test12"
    hashed = get_password_hash(password)
    verified = verify_password(password, hashed)
    print(f"✅ Fixed database module works: {verified}")
except Exception as e:
    print(f"❌ Fixed database module failed: {e}")

# Test 3: Original passlib approach (might show warning)
print("\n3. Testing original passlib approach:")
try:
    from database import get_password_hash as orig_hash, verify_password as orig_verify
    password = "test12"
    hashed = orig_hash(password)
    verified = orig_verify(password, hashed)
    print(f"✅ Original passlib works: {verified}")
except Exception as e:
    print(f"❌ Original passlib failed: {e}")

print("\n🎯 Recommendation: Use the approach that works without errors!")
