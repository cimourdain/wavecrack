# coding: utf8
import os

# third party imports
from flask import Blueprint, render_template

# local imports
from server import app

home_get = Blueprint('home_get', __name__, template_folder='templates')


@home_get.route('/', methods=["GET"])
def render_homepage():
    server_details = os.popen("uname -a").read() if app.config['DEBUG'] else None
    return render_template(
        "pages/home.html",
        title="Homepage",
        version=server_details
    )
