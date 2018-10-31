# standard imports
import pytest

# local imports
from app.tests import client
from app.tests.decorators import login_required


@pytest.mark.incremental
class TestAddRequestForm(object):

    @login_required()
    def test_form_is_active(self, client):
        response = client.get('/add')
        assert response.status_code == 200, "Add crack page cannot be reached"

