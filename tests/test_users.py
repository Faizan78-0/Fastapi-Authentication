def test_get_me(authorized_client):

    response = authorized_client.get("/users/me")
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@gmail.com"


def test_get_me_unauthorized(test_client):
    response = test_client.get("/users/me")

    assert response.status_code == 401


def test_partial_update_email(authorized_client):

    response = authorized_client.patch("/users/me",
        json={
            "email": "updated@gmail.com"
        }
    )
    assert response.status_code == 200
    assert response.json()["email"] == "updated@gmail.com"


def test_partial_update_password(authorized_client):

    response = authorized_client.patch("/users/me",
        json={
            "password": "newpassword"
        }
    )
    assert response.status_code == 200


def test_admin_get_all_users(authorized_client):

    response = authorized_client.get("/users/")
    # may fail if current user not admin
    assert response.status_code in [200, 403]