# coding: utf8
import os

# third party imports
from flask import Blueprint, render_template

# local imports
from server import app

ntds_upload_get = Blueprint('ntds_upload_get', __name__, template_folder='templates')


@ntds_upload_get.route('/ntds_upload', methods=["GET"])
def render_homepage():
    return render_template(
        "ntds_upload.html",
        title="Uploading NTDS files"
    )
