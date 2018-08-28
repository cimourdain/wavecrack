# coding: utf8
import os

# third party imports
from flask import Blueprint, render_template
from flask_login import login_required

# local imports
from server import app

add_get = Blueprint('add_get', __name__, template_folder='templates')


@add_get.route('/add', methods=["GET"])
@login_required
def new_hashes_form():
    server_details = os.popen("uname -a").read() if app.config['DEBUG'] else None
    return render_template(
        "homepage.html",
        title="Homepage",
        version=server_details
    )
