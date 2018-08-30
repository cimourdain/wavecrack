# coding: utf8
import os

# third party imports
from flask import Blueprint, render_template, jsonify
from flask_login import login_required

# local imports
from server import app
from app.forms.add_crack import AddCrackForm
from app.ref.hashes_list import HASHS_LIST

cracks_get = Blueprint('cracks_get', __name__, template_folder='templates')


@cracks_get.route('/add', methods=["GET"])
@login_required
def add_new_crack():
    return render_template(
        'cracks/add.html',
        title="Add new crack",
        form=AddCrackForm(),
        separator=app.config["HASHLIST_FILE_SEPARATOR"],
        hashes_list=HASHS_LIST[:10],  # used to populate javascript function
        max_len=app.config["MAX_CONTENT_LENGTH"]
    )
