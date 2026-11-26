def test_register_route(app):
    client = app.test_client()
    response = client.post('/api/auth/register', json={
        "nom": "Test User",
        "email": "test@example.com",
        "mot_de_passe": "password123"
    })
    assert response.status_code == 201
    data = response.get_json()
    assert data["utilisateur"]["email"] == "test@example.com"

def test_login_route(app):
    client = app.test_client()
    # Créer d'abord l'utilisateur
    client.post('/api/auth/register', json={
        "nom": "Test", "email": "login@test.com", "mot_de_passe": "pass123"
    })
    response = client.post('/api/auth/login', json={
        "email": "login@test.com", "mot_de_passe": "pass123"
    })
    assert response.status_code == 200
    assert "access_token" in response.get_json()