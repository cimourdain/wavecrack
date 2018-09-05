# coding: utf8
import os

# third party imports
from flask import Blueprint, jsonify

# local imports
from server import app
from app.classes.cmd import Cmd

test_get = Blueprint('test_get', __name__)


@test_get.route('/test', methods=["GET"])
def test_page():
    status, output, error = Cmd.run_cmd("ls -zz")
    return jsonify({
        "status": status,
        "output": output,
        "error": error
    })
