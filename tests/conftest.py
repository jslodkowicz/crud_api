import pytest

@pytest.fixture(scope="session")
def base_url():
    return "http://localhost:8000"

@pytest.fixture
def create_user(base_url):
    import requests
    def _create_user(name, email):
        payload = {"name": name, "email": email}
        response = requests.post(f"{base_url}/users", json=payload)
        assert response.status_code == 201
        return response.json()
    return _create_user