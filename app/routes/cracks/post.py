# coding: utf8
import os

# third party imports
from flask import Blueprint, render_template, jsonify, request, flash
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
            "wordlist_attack_type"
    ):
        form_is_valid = True

        # get hashes
        if "hashes_file" in request.form and FormHelper.uploaded_file_is_valid("hashes_file", [".txt"]):
            hashes = request.files["hashes_file"].read()
        else:
            hashes = request.form.get("hashes", "")

        # get hashtype code
        hash_type_code = int(request.form.get("hash_type"))

        # contains_usernames
        hashed_file_contains_usernames = int(request.form.get("hashed_file_contains_usernames", 0))

        # check attack_type
        attack_type = int(request.form.get("wordlist_attack_type"))
        if not attack_type:
            flash("Select one attack type.")
            form_is_valid = False

        attack_details = None
        if attack_type in [0, 1] :
            if not request.form.get("wordlist_file", None):
                flash("Select at least one word list for a wordlist attack")
                form_is_valid = False
            else:
                attack_details = request.form.get("wordlist_file", None)
        elif attack_type == 2:
            if not request.form.get("mask", None):
                flash("mask required", "error")
                form_is_valid = False
            elif not FormHelper.check_mask(request.form["mask"]):
                flash("mask invalid", "error")
                form_is_valid = False
            else:
                attack_details = request.form.get("mask", None)

        elif attack_type == 3:
            if not request.form.get("chosen_keywords", None):
                flash("Keywords required", "error")
                form_is_valid = False
            else:
                attack_details = request.form.get("keywords", None)
        elif attack_type == 4:
            bruteforce = int(request.form.get("bruteforce", 0))

        duration = int(request.form.get("duration", 3))

        if form_is_valid:
            return jsonify({"message": "display validation form"})

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
