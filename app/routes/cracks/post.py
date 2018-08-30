# coding: utf8
import os

# third party imports
from flask import Blueprint, render_template, jsonify, redirect, url_for, request
from flask_login import login_required

# local imports
from server import app
from app.forms.add_crack import AddCrackForm, WordListCheckBox
from app.ref.hashes_list import HASHS_LIST
from app.helpers.words import WordsHelper
from app.helpers.forms import FormHelper

cracks_post = Blueprint('cracks_post', __name__, template_folder='templates')


@cracks_post.route('/add', methods=["GET", "POST"])
@login_required
def add_new_crack():
    if request.method == "POST" and FormHelper.check_fields_in_form(
            ["hashes", "hashes_file"],
            ["keywords", "wordlist_attack_type"]
    ):
        return jsonify({"message": "display validation form"})
    else:
        return render_template(
            'cracks/add.html',
            title="Add new crack",
            form=AddCrackForm(request.form),
            wordlist_cb=WordListCheckBox(),
            separator=app.config["HASHLIST_FILE_SEPARATOR"],
            hashes_list=HASHS_LIST,  # used to populate javascript function
            max_len=app.config["MAX_CONTENT_LENGTH"],
            wordlist_files=WordsHelper.get_available_wordlists()
        )
