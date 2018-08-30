# coding: utf8
import os

# third party imports
from flask import Blueprint, render_template, jsonify
from flask_login import login_required

# local imports


hashes_get = Blueprint('hashes_get', __name__, template_folder='templates')


@hashes_get.route('/identify-hash', methods=["GET"])
def identify_hash():
    return render_template(
        "homepage.html",
        title="Homepage"
    )

