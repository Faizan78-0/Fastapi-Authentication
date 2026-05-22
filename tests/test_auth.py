
def test_register(test_client):
    response = test_client.post("/auth/register",
        json={
            "email": "new@gmail.com",
            "password": "123456"
        }
    )
    assert response.status_code == 201
    assert response.json()["message"] == "User created successfully"


def test_register_duplicate_email(test_client):
    test_client.post("/auth/register",
        json={
            "email": "duplicate@gmail.com",
            "password": "123456"
        }
    )

    response = test_client.post("/auth/register",
        json={
            "email": "duplicate@gmail.com",
            "password": "123456"
        }
    )
    assert response.status_code == 400


def test_login(test_client):
    test_client.post("/auth/register",
        json={
            "email": "login@gmail.com",
            "password": "123456"
        }
    )

    response = test_client.post("/auth/login",
        data={
            "username": "login@gmail.com",
            "password": "123456"
        }
    )

    data = response.json()
    assert response.status_code == 200
    assert "access_token" in data
    assert "refresh_token" in data


def test_invalid_login(test_client):
    response = test_client.post("/auth/login",
        data={
            "username": "wrong@gmail.com",
            "password": "wrong"
        }
    )

    assert response.status_code == 401


def test_refresh_token(test_client):
    test_client.post("/auth/register",
        json={
            "email": "refresh@gmail.com",
            "password": "123456"
        }
    )

    login = test_client.post("/auth/login",
        data={
            "username": "refresh@gmail.com",
            "password": "123456"
        }
    )
    refresh_token = login.json()["refresh_token"]

    response = test_client.post("/auth/refresh",
        params={
            "refresh_token": refresh_token
        }
    )
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_logout(test_client):
    test_client.post("/auth/register",
        json={
            "email": "logout@gmail.com",
            "password": "123456"
        }
    )

    login = test_client.post("/auth/login",
        data={
            "username": "logout@gmail.com",
            "password": "123456"
        }
    )

    refresh_token = login.json()["refresh_token"]


    response = test_client.post( "/auth/logout",
        params={
            "refresh_token": refresh_token
        }
    )
    assert response.status_code == 200


def test_forgot_password(test_client):

    test_client.post("/auth/register",
        json={
            "email": "forgot@gmail.com",
            "password": "123456"
        }
    )

    response = test_client.post("/auth/forgot_password",
        json={
            "email": "forgot@gmail.com"
        }
    )

    assert response.status_code in [200,403,404]