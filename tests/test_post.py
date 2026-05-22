def test_create_post(
    authorized_client
):

    response = authorized_client.post("/posts/",
        json={
            "title": "FastAPI",
            "content": "Testing posts"
        }
    )

    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "FastAPI"


def test_create_post_unauthorized(test_client):

    response = test_client.post("/posts/",
        json={
            "title": "Unauthorized",
            "content": "Should fail"
        }
    )
    assert response.status_code == 401



def test_get_all_posts_admin(authorized_client):
    response = authorized_client.get("/posts/all")
    assert response.status_code in [200,403, 404]