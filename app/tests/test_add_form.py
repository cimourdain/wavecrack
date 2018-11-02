# coding: utf8

# standard imports
from random import randint
from StringIO import StringIO

# third party imports
import pytest
from faker import Faker
import bs4 as BeautifulSoup

# local imports
from app.tests import client, app
from app.tests.decorators import login_required
from app.helpers.files import FilesHelper
from app.ref.hashes_list import HASHS_CODES_LIST

fake = Faker()


@pytest.mark.incremental
class TestAddRequestForm(object):

    form_url = '/add'

    MISSING_NAME_MESSAGE = 'Request name required'
    MISSING_HASH_MESSAGE = 'Hashes or hash file required'
    MISSING_ATTACK_MESSAGE = "Select at least one attack type"
    INVALID_MASK_MESSAGE = "Empty or invalid mask"
    INVALID_HASH_CODE_MESSAGE = "Invalid hash code"
    MISSING_RULE_FILE_MESSAGE = "To apply rules, select at least one rule in Options tab"

    @staticmethod
    def check_message_in_response(response_txt, message, expected=True):
        assert (message in response_txt) == expected, \
            "Message \""+str(message) + "\" not found in response" if expected else \
            "Message \""+str(message) + "\" found in response"

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

        TestAddRequestForm.check_message_in_response(
            response_txt=response_txt,
            message=TestAddRequestForm.MISSING_NAME_MESSAGE
        )
        TestAddRequestForm.check_message_in_response(
            response_txt=response_txt,
            message=TestAddRequestForm.MISSING_HASH_MESSAGE
        )
        TestAddRequestForm.check_message_in_response(
            response_txt=response_txt,
            message=TestAddRequestForm.MISSING_ATTACK_MESSAGE
        )

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
        TestAddRequestForm.check_message_in_response(
            response_txt=response_txt,
            message=TestAddRequestForm.MISSING_NAME_MESSAGE,
            expected=False
        )

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
        TestAddRequestForm.check_message_in_response(
            response_txt=response_txt,
            message=TestAddRequestForm.MISSING_HASH_MESSAGE,
            expected=False
        )

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
        TestAddRequestForm.check_message_in_response(
            response_txt=response_txt,
            message=TestAddRequestForm.MISSING_HASH_MESSAGE,
            expected=False
        )

        # check that input content matches new name
        soup = BeautifulSoup.BeautifulSoup(response_txt, 'html.parser')
        name_input = soup.find("textarea", {"id": "hashes"})
        assert name_input, "hashes textarea not found"
        assert name_input.getText() == file_content, "Form hashes does not match input value"

    @login_required()
    def test_invalid_hash_code(self, client):
        # get invalid hash code
        hash_codes_ref_list = [int(c["code"]) for c in HASHS_CODES_LIST]
        hash_code = hash_codes_ref_list[0]
        while hash_code in hash_codes_ref_list:
            hash_code = randint(min(hash_codes_ref_list), max(hash_codes_ref_list))

        response = client.post(
            TestAddRequestForm.form_url,
            follow_redirects=True,
            data={
                "hash_type": hash_code,
            }
        )
        response_txt = response.get_data(as_text=True).encode('ascii', 'ignore')
        TestAddRequestForm.check_message_in_response(
            response_txt,
            message=TestAddRequestForm.INVALID_HASH_CODE_MESSAGE,
            expected=True
        )

    @login_required()
    def test_valid_dict_attack(self, client):
        """
        Test that when dicts are selected, no error is raised
        :param client:
        :return:
        """
        dicts = []
        for f in FilesHelper.get_available_files(app.config["DIR_LOCATIONS"]["wordlists"]):
            dicts.append(f)
        assert dicts, "No dictionary found in "+str(app.config["DIR_LOCATIONS"]["wordlists"])

        response = client.post(
            TestAddRequestForm.form_url,
            follow_redirects=True,
            data={
                "wordlist_files": dicts,
            }
        )
        response_txt = response.get_data(as_text=True).encode('ascii', 'ignore')
        TestAddRequestForm.check_message_in_response(
            response_txt,
            message=TestAddRequestForm.MISSING_ATTACK_MESSAGE,
            expected=False
        )

    @login_required()
    def test_valid_dict_attack(self, client):
        """
        Test that when dicts are selected, no error is raised
        :param client:
        :return:
        """
        dicts = []
        for f in FilesHelper.get_available_files(app.config["DIR_LOCATIONS"]["wordlists"]):
            dicts.append(f)
        assert dicts, "No dictionary found in " + str(app.config["DIR_LOCATIONS"]["wordlists"])

        response = client.post(
            TestAddRequestForm.form_url,
            follow_redirects=True,
            data={
                "wordlist_files": dicts,
            }
        )
        response_txt = response.get_data(as_text=True).encode('ascii', 'ignore')
        TestAddRequestForm.check_message_in_response(
            response_txt=response_txt,
            message=TestAddRequestForm.MISSING_ATTACK_MESSAGE,
            expected=False
        )

    @login_required()
    def test_invalid_mask_attack(self, client):
        """
        Test that when mask are selected, no error is raised
        :param client:
        :return:
        """
        response = client.post(
            TestAddRequestForm.form_url,
            follow_redirects=True,
            data={
                "mask": "toto?ztiti",
            }
        )
        response_txt = response.get_data(as_text=True).encode('ascii', 'ignore')
        TestAddRequestForm.check_message_in_response(
            response_txt=response_txt,
            message=TestAddRequestForm.INVALID_MASK_MESSAGE,
            expected=True
        )

    @login_required()
    def test_valid_mask_attack(self, client):
        """
        Test that when mask are selected, no error is raised
        :param client:
        :return:
        """
        response = client.post(
            TestAddRequestForm.form_url,
            follow_redirects=True,
            data={
                "mask": fake.text().encode('utf-8') + "?u?l?d?h?H?s?a?b",
            }
        )
        response_txt = response.get_data(as_text=True).encode('ascii', 'ignore')
        TestAddRequestForm.check_message_in_response(
            response_txt=response_txt,
            message=TestAddRequestForm.MISSING_ATTACK_MESSAGE,
            expected=False
        )

    @login_required()
    def test_bruteforce_attack(self, client):
        """
        Test that when bruteforce are selected, no error is raised
        :param client:
        :return:
        """
        response = client.post(
            TestAddRequestForm.form_url,
            follow_redirects=True,
            data={
                "bruteforce": "y",
            }
        )
        response_txt = response.get_data(as_text=True).encode('ascii', 'ignore')
        TestAddRequestForm.check_message_in_response(
            response_txt=response_txt,
            message=TestAddRequestForm.MISSING_ATTACK_MESSAGE,
            expected=False
        )

    @login_required()
    def test_rules_without_file_selected(self, client):
        response = client.post(
            TestAddRequestForm.form_url,
            follow_redirects=True,
            data={
                "rules": "y",
                "rules_files": []
            }
        )
        response_txt = response.get_data(as_text=True).encode('ascii', 'ignore')
        TestAddRequestForm.check_message_in_response(
            response_txt=response_txt,
            message=TestAddRequestForm.MISSING_RULE_FILE_MESSAGE,
            expected=True
        )

    @login_required()
    def test_rules_with_file_selected(self, client):
        rules_files = []
        for f in FilesHelper.get_available_files(app.config["DIR_LOCATIONS"]["rules"]):
            rules_files.append(f)
        assert rules_files, "No rule file found in " + str(app.config["DIR_LOCATIONS"]["rules"])

        response = client.post(
            TestAddRequestForm.form_url,
            follow_redirects=True,
            data={
                "rules": "y",
                "rules_files": rules_files
            }
        )
        response_txt = response.get_data(as_text=True).encode('ascii', 'ignore')
        TestAddRequestForm.check_message_in_response(
            response_txt=response_txt,
            message=TestAddRequestForm.MISSING_RULE_FILE_MESSAGE,
            expected=False
        )
