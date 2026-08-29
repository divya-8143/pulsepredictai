import pytest
from app.core.security import verify_password, get_password_hash, create_access_token, decode_token

def test_password_hashing_and_verification():
    raw_password = "SecurePassword2026!"
    hashed = get_password_hash(raw_password)
    
    assert hashed != raw_password
    assert verify_password(raw_password, hashed) is True
    assert verify_password("WrongPassword!", hashed) is False

def test_jwt_token_creation_and_decoding():
    user_id = "12345678-1234-5678-1234-567812345678"
    role = "PATIENT"
    token = create_access_token(user_id, role)
    
    payload = decode_token(token)
    assert payload["sub"] == user_id
    assert payload["role"] == role
    assert payload["type"] == "access"
