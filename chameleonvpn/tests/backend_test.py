def test_api_root(client):
    response = client.get("/")
    assert response.status_code == 200

def test_login(client):
    resp = client.post("/auth/login", json={"email": "test@test.com", "password": "test"})
    assert resp.status_code == 200
