import requests
import pytest

def test_get_users_returns_list_and_status_200(base_url):
    response = requests.get(f"{base_url}/users")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

def test_create_user_returns_201_and_correct_data(base_url):
    payload = {"name": "Alice", "email": "alice@email.com"}
    response = requests.post(f"{base_url}/users", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Alice"
    assert data["email"] == "alice@email.com"

def test_create_and_get_user_by_id(created_users, base_url):
    created_user = created_users("Bob", "bob@email.com")
    user_id = created_user.get("id")
    assert user_id is not None

    get_resp = requests.get(f"{base_url}/users/{user_id}")
    assert get_resp.status_code == 200
    fetched_user = get_resp.json()
    assert fetched_user["name"] == "Bob"
    assert fetched_user["email"] == "bob@email.com"
    assert fetched_user["id"] == user_id

def test_update_user(created_users, base_url):
    created_user = created_users("Charlie", "charlie@email.com")
    user_id = created_user.get("id")
    assert user_id is not None

    update_payload = {"name": "Charlie Updated", "email": "charlie.updated@email.com"}
    update_resp = requests.put(f"{base_url}/users/{user_id}", json=update_payload)
    assert update_resp.status_code == 200

    get_resp = requests.get(f"{base_url}/users/{user_id}")
    assert get_resp.status_code == 200
    fetched_user = get_resp.json()
    assert fetched_user["name"] == update_payload["name"]
    assert fetched_user["email"] == update_payload["email"]
    assert fetched_user["id"] == user_id

@pytest.mark.parametrize(
    "payload,expected_status",
    [
        ({"name": "Valid User", "email": "valid@email.com"}, 201),
        ({"name": "No Email"}, 422),
        ({"email": "no_name@email.com"}, 422),
        ({}, 422),
        ({"name": 123, "email": "valid@email.com"}, 422),
        ({"name": "Valid User", "email": 456}, 422),
        ({"name": ["list"], "email": "valid@email.com"}, 422),
        ({"name": "Valid User", "email": ["list@email.com"]}, 422),
        ({"name": None, "email": "valid@email.com"}, 422),
        ({"name": "Valid User", "email": None}, 422),
    ]
)
def test_create_user_parametrized(base_url, payload, expected_status):
    # We don't use the create_user fixture here because we want to test various payloads,
    # including invalid ones, to verify input validation and error handling.
    # The create_user fixture likely assumes valid input and may not handle error cases as needed.
    response = requests.post(f"{base_url}/users", json=payload)
    assert response.status_code == expected_status
