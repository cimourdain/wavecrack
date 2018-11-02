# coding: utf8

# third party imports
import pytest
from faker import Faker
import bs4 as BeautifulSoup

# local imports
from app.tests import client, app
from app.tests.decorators import login_required
from app.helpers.files import FilesHelper

fake = Faker()


@pytest.mark.incremental
class TestSubmitNewRequestForm(object):
    form_url = '/add'

    @staticmethod
    def get_page_title(response_txt, expected_title=""):
        soup = BeautifulSoup.BeautifulSoup(response_txt, 'html.parser')
        page_title = soup.find("h1")
        assert page_title.getText() == expected_title

    @login_required()
    def test_sumbit_valid_form(self, client):
        dicts = []
        for f in FilesHelper.get_available_files(app.config["DIR_LOCATIONS"]["wordlists"]):
            dicts.append(f)
        assert dicts, "No dictionary found in " + str(app.config["DIR_LOCATIONS"]["wordlists"])

        response = client.post(
            TestSubmitNewRequestForm.form_url,
            follow_redirects=True,
            data={
                "request_name": fake.words(),
                "hashes": """f02368945726d5fc2a14eb576f7276c0
                    88bf9b7a14efd3dcf4aea0aaf8a80752
                    81dc9bdb52d04dc20036dbd8313ed055
                    dab9cc56c236a72ad4517e3833c20073
                    c171d6ff4b15af44e859f0decf5f0d44
                    8d8d7daf8afbc3257f249f0d6f8df92d
                    89c447228de18900b8cf6433ba885fe6
                    4124bc0a9335c27f086f24ba207a4912""",
                "hashes_type": 0,
                "wordlist_files": dicts,
                "confirm_btn": "y"
            }
        )
        assert response.status_code == 200, "Form cannot be submitted"
        TestSubmitNewRequestForm.get_page_title(
            response_txt=response.get_data(as_text=True).encode('ascii', 'ignore'),
            expected_title="All your cracks"
        )