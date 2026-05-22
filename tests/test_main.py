def test_logging_middleware(test_client):
    response = test_client.get("/")

    assert response.status_code == 200