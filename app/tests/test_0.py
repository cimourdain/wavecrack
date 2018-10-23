# standard imports
import subprocess
import shlex

# local imports
from app.tests import client
from config import TestingConfig


def test_website_reacheable(client):
    """
    Check that app is launched

    :return:
    """
    response = client.get('/')
    assert response.status_code == 200, "Homepage cannot be reached"


def test_hashcat_available(client):
    """
    Check that hashcat application is reachable

    :param client:
    :return:
    """
    cmd = TestingConfig.APP_LOCATIONS["hashcat"] + " --version"
    out = subprocess.check_output(shlex.split(cmd))

    assert out, "Impossible to launch hashcat"
    assert "v" in out, "Impossible to get hashcat version"
