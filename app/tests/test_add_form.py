# coding: utf8
# standard imports
import pytest

# local imports
from app.tests import client
from app.tests.decorators import login_required


@pytest.mark.incremental
class TestAddRequestForm(object):

    form_url = '/add'

    @staticmethod
    def response_contains_missing_name_error(response_txt):
        assert 'Request name required' in response_txt, "No Error for missing name in form in add request form"

    @staticmethod
    def response_contains_missing_hash_error(response_txt):
        assert 'Hashes or hash file required' in response_txt, "No Error for missing hash in add request form"

    @staticmethod
    def response_contains_missing_attack_error(response_txt):
        # assert 'Select at least one attack type' in response_txt, "No Error for missing attack in add request form"
        assert "Select at" in response_txt, "No Error for missing hash in add request form \n"+str(response_txt)

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
