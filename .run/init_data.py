import requests
import time

url = "https://opensoar.local/api"
requests.post(
    f"{url}/auth/register",
    json={"email": "ada@lovelace.com", "password": "123"},
    verify=False,
)
time.sleep(1)
r = requests.post(
    f"{url}/auth/jwt/login",
    data={"username": "ada@lovelace.com", "password": "123"},
    verify=False,
)
print(r.text)
token = r.json()["access_token"]
r = requests.get(
    f"{url}/users/me", headers={"Authorization": f"Bearer {token}"}, verify=False
)
user = r.json()["id"]

for _ in range(26):
    requests.post(
        f"{url}/incidents",
        json={
            "title": "bad stuff",
            "owner_id": f"{user}",
            "description": """Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.""",
            "status": "New",
        },
        headers={"Authorization": f"Bearer {token}"},
        verify=False,
    )

requests.post(
    f"{url}/auth/register",
    json={"email": "bob@lovelace.com", "password": "123"},
    verify=False,
)
r = requests.post(
    f"{url}/auth/jwt/login",
    data={"username": "bob@lovelace.com", "password": "123"},
    verify=False,
)
token = r.json()["access_token"]
r = requests.get(
    f"{url}/users/me", headers={"Authorization": f"Bearer {token}"}, verify=False
)
user = r.json()["id"]

for _ in range(26):
    requests.post(
        f"{url}/incidents",
        json={
            "title": "bad stuff",
            "owner_id": f"{user}",
            "description": """Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.""",
            "status": "New",
        },
        headers={"Authorization": f"Bearer {token}"},
        verify=False,
    )
