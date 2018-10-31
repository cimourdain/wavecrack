# coding: utf8

# standard imports
from StringIO import StringIO

# third party imports
import pytest
from faker import Faker
import bs4 as BeautifulSoup

# local imports
from app.tests import client
from app.tests.decorators import login_required

fake = Faker()


@pytest.mark.incremental
class TestAddRequestForm(object):

    form_url = '/add'

    @staticmethod
    def response_contains_missing_name_error(response_txt, expected=True):
        assert ('Request name required' in response_txt) == expected, \
            "No Error for missing name in form in add request form" if expected else \
            "Error for missing name found in form in add request form"

    @staticmethod
    def response_contains_missing_hash_error(response_txt, expected=True):
        assert ('Hashes or hash file required' in response_txt) == expected, \
            "No Error for missing hash in add request form" if expected else \
            "Error for missing hash found in add request form"

    @staticmethod
    def response_contains_missing_attack_error(response_txt, expected=True):
        assert ("Select at least one attack type" in response_txt) == expected, \
            "No Error for missing hash in add request form" if expected else \
            "Error for missing hash found in add request form"

    @login_required()
    def test_form_is_active(self, client):
        """
        Test that add request page is available

        :param client: <FlaskClient>
        :return:
        """
        response = client.get(TestAddRequestForm.form_url)
        assert response.status_code == 200, "Add crack page cannot be reached"

    @login_required()
    def test_form_empty_submit(self, client):
        """
        Test that empty form submission raise errors :
            - Missing request name error
            - Missing hashes error
            - Missing attack error

        :param client:<FlaskClient>
        :return:
        """
        response = client.post(TestAddRequestForm.form_url, follow_redirects=True)
        response_txt = response.get_data(as_text=True).encode('ascii', 'ignore')

        TestAddRequestForm.response_contains_missing_name_error(response_txt)
        TestAddRequestForm.response_contains_missing_hash_error(response_txt)
        TestAddRequestForm.response_contains_missing_attack_error(response_txt)

    @login_required()
    def test_valid_name(self, client):
        """
        Check that if request name is not empty, the missing name error message is not displayed on submit
        :param client: <FlaskClient>
        :return:
        """
        name = fake.sentence(nb_words=6)
        response = client.post(
            TestAddRequestForm.form_url,
            follow_redirects=True,
            data={
                "request_name": name
            }
        )
        response_txt = response.get_data(as_text=True).encode('ascii', 'ignore')
        TestAddRequestForm.response_contains_missing_name_error(response_txt, expected=False)

        # check that input content matches new name
        soup = BeautifulSoup.BeautifulSoup(response_txt, 'html.parser')
        name_input = soup.find("input", {"id": "request_name"})
        assert name_input, "Name input not found"
        assert name_input['value'] == name, "Form name does not match input name"

    @login_required()
    def test_valid_hashes_textarea(self, client):
        """
        Check that if hashes textarea is not empty, the missing hashes error message is not displayed on submit
        :param client: <FlaskClient>
        :return:
        """
        new_hashes = fake.text()
        response = client.post(
            TestAddRequestForm.form_url,
            follow_redirects=True,
            data={
                "hashes": new_hashes
            }
        )
        response_txt = response.get_data(as_text=True).encode('ascii', 'ignore')
        TestAddRequestForm.response_contains_missing_hash_error(response_txt, expected=False)

        # check that input content matches new name
        soup = BeautifulSoup.BeautifulSoup(response_txt, 'html.parser')
        name_input = soup.find("textarea", {"id": "hashes"})
        assert name_input, "hashes textarea not found"
        assert name_input.getText() == new_hashes, "Form hashes does not match input value"

    @login_required()
    def test_valid_hashes_file(self, client):
        """
        Check that if hashes textarea is not empty, the missing hashes error message is not displayed on submit
        :param client: <FlaskClient>
        :return:
        """
        file_content = fake.text().encode('utf-8')
        response = client.post(
            TestAddRequestForm.form_url,
            follow_redirects=True,
            data={
                "hashes_file": (StringIO(file_content), 'hashes_file.txt'),
            }
        )
        response_txt = response.get_data(as_text=True).encode('ascii', 'ignore')
        TestAddRequestForm.response_contains_missing_hash_error(response_txt, expected=False)

        # check that input content matches new name
        soup = BeautifulSoup.BeautifulSoup(response_txt, 'html.parser')
        name_input = soup.find("textarea", {"id": "hashes"})
        assert name_input, "hashes textarea not found"
        assert name_input.getText() == file_content, "Form hashes does not match input value"

