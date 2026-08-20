from app.core.security import create_access_token, decode_access_token

def test_create_and_decode_access_token():
    data = {"sub": "1", "tenant_id": 1}
    token = create_access_token(data=data)
    
    assert isinstance(token, str)
    assert len(token) > 0
    
    decoded = decode_access_token(token)
    assert decoded["tenant_id"] == 1
    assert decoded["sub"] == "1"
    assert "exp" in decoded

def test_tenant_isolation_in_token():
    # Token for tenant 1
    token1 = create_access_token(data={"sub": "1", "tenant_id": 1})
    decoded1 = decode_access_token(token1)
    assert decoded1["tenant_id"] == 1
    
    # Token for tenant 2
    token2 = create_access_token(data={"sub": "2", "tenant_id": 2})
    decoded2 = decode_access_token(token2)
    assert decoded2["tenant_id"] == 2
    
    assert decoded1["tenant_id"] != decoded2["tenant_id"]
