import requests
import pytest

def test_get_users_returns_list(base_url):
    response = requests.get(f"{base_url}/users")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_create_user_returns_created_user(base_url):
    payload = {"name": "Tom", "email": "tom@email.com"}
    response = requests.post(f"{base_url}/users", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Tom"
    assert data["email"] == "tom@email.com"

@pytest.mark.parametrize(
    "payload,expected_status",
    [
        ({"name": "Alice", "email": "alice@email.com"}, 201),
        ({"name": "", "email": "bob@email.com"}, 201),
        ({"name": "Charlie", "email": ""}, 201),
        ({"email": "eve@email.com"}, 422),
        ({"name": "Frank"}, 422),
        ({}, 422),
        ({"name": "Grace", "email": "not-an-email"}, 201),
        ({"name": 123, "email": "number@email.com"}, 422),
        ({"name": "Henry", "email": 456}, 422),
        ({"name": None, "email": "none@email.com"}, 422),
        ({"name": "Ivy", "email": None}, 422),
        ({"name": ["list"], "email": "list@email.com"}, 422),
        ({"name": "Jack", "email": ["list@email.com"]}, 422),
        ({"name": {"first": "John"}, "email": "dict@email.com"}, 422),
        ({"name": "Kate", "email": {"address": "dict@email.com"}}, 422),
    ],
)
def test_create_user_parametrized(base_url, payload, expected_status):
    response = requests.post(f"{base_url}/users", json=payload)
    assert response.status_code == expected_status
