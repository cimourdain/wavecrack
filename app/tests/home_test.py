# local imports
from app.tests import client
from config import TestingConfig


class TestLogin(object):

    random_valid_admin = None
    random_valid_user = None

    @staticmethod
    def user_is_logged(response):
        """
        Method to test if response (html page) contains element allowing to consider user is logged
        :param response:
        :return:
        """
        if 'Invalid login' in response.get_data(as_text=True):
            print("Invalid login error message found in page")
            return False

        if 'Logout' not in response.get_data(as_text=True):
            print("Logout link not found")
            return False

        if 'New crack' not in response.get_data(as_text=True):
            print("New crack menu entry not found")
            return False

        return True

    @staticmethod
    def login(client, user_data):
        """
        method to attempt login on client (test client) with user_data
        :param client: <Flask> client
        :param user_data: <dict> containing login and password keys
        :return:<bool>
        """
        response = client.post('/login', data=user_data, follow_redirects=True)

        assert TestLogin.user_is_logged(response), \
            "Impossible to login with user: {} and password: {}".format(
                user_data["login"],
                user_data["password"]
            )

        return True

    def test_set_valid_admin_user(self):
        """
        Method to define random_valid_admin and random_valid_user from config default users
        :return:
        """
        for u in TestingConfig.DEFAULT_USERS:
            if not self.random_valid_admin and u["admin"]:
                TestLogin.random_valid_admin = u
            if not self.random_valid_user and not u["admin"]:
                TestLogin.random_valid_user = u

            if self.random_valid_user and self.random_valid_admin:
                break

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
