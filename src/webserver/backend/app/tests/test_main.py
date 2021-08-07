import requests
import requests.cookies
import requests.auth
import random
import typing

# Annotations for `Session.request()`
Cookies = typing.Union[
    typing.MutableMapping[str, str], requests.cookies.RequestsCookieJar
]
Params = typing.Union[bytes, typing.MutableMapping[str, str]]
DataType = typing.Union[bytes, typing.MutableMapping[str, str], typing.IO]
TimeOut = typing.Union[float, typing.Tuple[float, float]]
FileType = typing.MutableMapping[str, typing.IO]
AuthType = typing.Union[
    typing.Tuple[str, str],
    requests.auth.AuthBase,
    typing.Callable[[requests.Request], requests.Request],
]


class Client(requests.Session):
    def __init__(self, base_url):
        self.base_url = base_url
        super(Client, self).__init__()

    def request(  # type: ignore
        self,
        method: str,
        url: str,
        params: Params = None,
        data: DataType = None,
        headers: typing.MutableMapping[str, str] = None,
        cookies: Cookies = None,
        files: FileType = None,
        auth: AuthType = None,
        timeout: TimeOut = None,
        allow_redirects: bool = None,
        proxies: typing.MutableMapping[str, str] = None,
        hooks: typing.Any = None,
        stream: bool = None,
        verify: typing.Union[bool, str] = None,
        cert: typing.Union[str, typing.Tuple[str, str]] = None,
        json: typing.Any = None,
    ) -> requests.Response:
        url = self.base_url + url
        return super().request(
            method,
            url,
            params=params,
            data=data,
            headers=headers,
            cookies=cookies,
            files=files,
            auth=auth,
            timeout=timeout,
            allow_redirects=allow_redirects,
            proxies=proxies,
            hooks=hooks,
            stream=stream,
            verify=verify,
            cert=cert,
            json=json,
        )


client = Client(base_url="http://opensoar.local/api")


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {}


def test_create_user():
    rnd = random.randint(0, 1000)
    response = client.post(
        "/users", json={"email": f"ada+{rnd}@test.com", "password": "password"}
    )
    if not response.ok:
        print(response.text)
        assert False
    user_id = response.json()["id"]
    assert response.status_code == 201
    assert response.json() == {
        "id": user_id,
        "email": f"ada+{rnd}@test.com",
        "is_active": True,
        "incidents": [],
    }
    response = client.post(
        "/users", json={"email": f"ada+{rnd}@test.com", "password": "password"}
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Email already registered"}


def test_read_users():
    response = client.get("/users")
    assert response.status_code == 200
    assert type(response.json()) == list


def test_read_user():
    rnd = random.randint(0, 1000)
    response = client.post(
        "/users", json={"email": f"ada+{rnd}@test.com", "password": "password"}
    )
    if not response.ok:
        print(response.text)
        assert False
    user_id = response.json()["id"]
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    assert response.json() == {
        "id": user_id,
        "email": f"ada+{rnd}@test.com",
        "is_active": True,
        "incidents": [],
    }


def test_create_incident_for_user():
    rnd = random.randint(0, 1000)
    response = client.post(
        "/users", json={"email": f"ada+{rnd}@test.com", "password": "password"}
    )
    if not response.ok:
        print(response.text)
        assert False
    user_id = response.json().copy()["id"]
    response = client.post(
        f"/users/{user_id}/incidents", json={"title": "new incident for ada"}
    )
    assert response.status_code == 201
    incident_id = response.json()["id"]
    assert response.json() == {
        "title": "new incident for ada",
        "description": None,
        "id": incident_id,
        "owner_id": user_id,
    }


def test_read_incidents():
    rnd = random.randint(0, 1000)
    response = client.post(
        "/users", json={"email": f"ada+{rnd}@test.com", "password": "password"}
    )
    if not response.ok:
        print(response.text)
        assert False
    user_id = response.json()["id"]
    response = client.post(
        f"/users/{user_id}/incidents", json={"title": "new incident for ada"}
    )
    if not response.ok:
        print(response.text)
        assert False
    response = client.get("/incidents")
    assert response.status_code == 200
    assert type(response.json()) == list
