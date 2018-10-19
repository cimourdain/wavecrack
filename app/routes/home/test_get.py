from tests.pytest_init import client


def test_home(client):
    response = client.get('/')
    assert response.status_code == 200, "Homepage cannot be reached"
    assert ('Login' in response.get_data(as_text=True)), "Login not found"
