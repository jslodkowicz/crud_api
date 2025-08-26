import pytest
import requests

@pytest.fixture(scope="session")
def base_url():
    return "http://localhost:8000"

@pytest.fixture
def created_users(base_url, request):
    user_ids = []

    def _create_user(name, email):
        payload = {"name": name, "email": email}
        response = requests.post(f"{base_url}/users", json=payload)
        assert response.status_code == 201
        user = response.json()
        user_ids.append(user["id"])
        return user

    def cleanup():
        for user_id in user_ids:
            requests.delete(f"{base_url}/users/{user_id}")

    request.addfinalizer(cleanup)
    return _create_user