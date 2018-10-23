# local imports
from app.tests import client
from config import TestingConfig


class TestLogin(object):

    random_valid_admin = None
    random_valid_user = None

    @staticmethod
    def user_is_logged(response, admin=False):
        """
        Method to test if response (html page) contains element allowing to consider user is logged
        :param response: response from client.get()
        :param admin: <bool> check if client is admin
        :return:
        """
        assert 'Invalid login' not in response.get_data(as_text=True), "Invalid login error message found in page"

        assert 'Logout' in response.get_data(as_text=True), "Logout link not found"

        assert 'New crack' in response.get_data(as_text=True), "New crack menu entry not found"

        if admin:
            assert 'All Cracks' in response.get_data(as_text=True), "All Crack entry menu not found for admin"

        return True

    @staticmethod
    def login(client, user_data=None, admin=True):
        """
        method to attempt login on client (test client) with user_data
        :param client: <Flask> client
        :param user_data: <dict> containing login and password keys
        :param admin: <bool> user is admin
        :return:<bool>
        """
        if not user_data:
            user = TestLogin.get_user_credentials_from_config(admin=admin)
            assert user, "Impossible to find user in config"
            user_data = {
                "login": user["name"],
                "password": user["password"]
            }

        response = client.post('/login', data=user_data, follow_redirects=True)

        TestLogin.user_is_logged(response), \
            "Impossible to login with user: {} and password: {}".format(
                user_data["login"],
                user_data["password"]
            )

        return True

    @staticmethod
    def get_user_credentials_from_config(admin=False):
        for u in TestingConfig.DEFAULT_USERS:
            if u["admin"] == admin:
                return u

        return None

    def test_init(self):
        """
        Method to define random_valid_admin and random_valid_user from config default users
        :return:
        """
        TestLogin.random_valid_user = TestLogin.get_user_credentials_from_config()
        TestLogin.random_valid_admin = TestLogin.get_user_credentials_from_config(admin=True)

        assert self.random_valid_user, "No config default user found"
        assert self.random_valid_admin, "No config default admin found"

    def test_is_logout(self, client):
        """
        perform logout before starting all tests
        """
        client.get('/logout')
        response = client.get('/')
        assert ('Login' in response.get_data(as_text=True)), "Login not found"

    def test_no_post_data_login(self, client):
        """
        Check that logging without data fail
        """
        response = client.post('/login', data={}, follow_redirects=True)

        assert ('Invalid login' in response.get_data(as_text=True)), "Invalid login error message not found"

    def test_empty_login(self, client):
        """
        Check that logging with empty data fails
        """
        response = client.post('/login', data={"login": "", "password": ""}, follow_redirects=True)

        assert ('Invalid login' in response.get_data(as_text=True)), "Invalid login error message not found"

    def test_invalid_login(self, client):
        """
        Check that logging with invalid credentials fails
        """
        response = client.post('/login', data={"login": "toto", "password": "toto"}, follow_redirects=True)

        assert ('Invalid login' in response.get_data(as_text=True)), "Invalid login error message not found"

    def test_valid_non_admin_login_by_name(self, client):
        """
        Check that users can connect with login/password
        """
        TestLogin.login(client, {
            "login": self.random_valid_user["name"],
            "password": self.random_valid_user["password"]
        })

        client.get('/logout')

    def test_valid_non_admin_login_by_email(self, client):
        """
        Check that user can connect with email/password
        """
        TestLogin.login(client, {
            "login": self.random_valid_user["email"],
            "password": self.random_valid_user["password"]
        })

        client.get('/logout')

    def test_valid_admin_login_by_name(self, client):
        """
        Check that admin can connect with login/password
        """
        TestLogin.login(client, {
            "login": self.random_valid_admin["name"],
            "password": self.random_valid_admin["password"]
        })

        client.get('/logout')

    def test_valid_admin_login_by_email(self, client):
        """
        Check that admin can connect with email/password
        """
        TestLogin.login(client, {
            "login": self.random_valid_admin["email"],
            "password": self.random_valid_admin["password"]
        })

        client.get('/logout')
