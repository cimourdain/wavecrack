# coding: utf8
import os

# third party imports
from flask import Blueprint, render_template, jsonify, request, flash
from flask_login import login_required

# local imports
from server import app
from app.forms.add_crack import AddCrackForm
from app.ref.hashes_list import HASHS_LIST
from app.helpers.words import WordsHelper
from app.helpers.forms import FormHelper

cracks_post = Blueprint('cracks_post', __name__, template_folder='templates')


def get_wordlists_cb(name):
    """
    function used to create a list of dictionary based on list of word files

    list returned is used in template to generate files checkboxes

    name parameter is either used to build file list for classic dict attack or for variation dict attack
    """
    wordlist_cb = []
    for wordfile in WordsHelper.get_available_wordlists():
        sumbitted_values = request.form.get(name, None)
        wordlist_cb.append({
            'name': name,
            'label': wordfile,
            'value': wordfile,
            'checked': True if sumbitted_values and wordfile in sumbitted_values else False
        })
    return wordlist_cb


def render_add_page(message=None, current_hashes="", confirmation=False):
    """
    function used to render add template page
    """
    if message:
        # if error message flash it
        flash(message, 'error')

    form = AddCrackForm(request.form)
    if current_hashes:
        print("set hashes to "+str(current_hashes))
        form.hashes.data = current_hashes

    # render add form
    return render_template(
        'cracks/add.html',
        title="Add new crack" if not confirmation else "Confirm new crack",
        form=form,
        separator=app.config["HASHLIST_FILE_SEPARATOR"],
        hashes_list=HASHS_LIST,  # used to populate javascript function
        max_len=app.config["MAX_CONTENT_LENGTH"],
        wordlist_cb_classic=get_wordlists_cb('attack_classic_dict_files'),
        wordlist_cb_variations=get_wordlists_cb('attack_variations_dict_files'),
        confirmation=confirmation
    )


@cracks_post.route('/add', methods=["GET", "POST"])
@login_required
def add_new_crack():
    if request.method == "POST" and FormHelper.check_fields_in_form(
            ["hashes", "hashes_file"]
    ):
        form_is_valid = True

        # get hashes
        hashes = request.form.get("hashes", "")
        if "hashes_file" in request.files and FormHelper.uploaded_file_is_valid("hashes_file", [".txt"]):
            print("Upload file")
            hashes = request.files["hashes_file"].read()
            print("Hashes : "+str(hashes))

        # get hashtype code
        hash_type_code = int(request.form.get("hash_type"))

        # contains_usernames
        hashed_file_contains_usernames = request.form.get("hashed_file_contains_usernames", 'n')

        # check selected attack_types
        # keywords
        attack_keywords = request.form.get('attack_mode_keywords_cb', None)
        keywords = request.form.get('keywords', None)
        if attack_keywords and not keywords:
            return render_add_page("Keywords list required")

        # classic dict attack
        attack_dict_classic = request.form.get('attack_mode_dict_classic_cb', None)
        attack_classic_dict_files = request.form.get('attack_classic_dict_files', None)
        if attack_dict_classic and not attack_classic_dict_files:
            return render_add_page("List of dict required for classic dict attack")

        # variation dict attack
        attack_dict_variation = request.form.get('attack_mode_dict_variations_cb', None)
        attack_variations_dict_files = request.form.get('attack_variations_dict_files', None)
        if attack_dict_variation and not attack_variations_dict_files:
            return render_add_page("List of dict required for variations dict attack")

        # mask attack
        attack_mask = request.form.get('attack_mode_mask_cb', None)
        mask = request.form.get('mask', None)
        if attack_mask and not mask:
            return render_add_page("mask required")

        # bruteforce attack
        attack_bruteforce = request.form.get('attack_mode_bruteforce_cb', None)

        # check that at least one attack mode was selected
        if not attack_keywords and not attack_dict_classic \
                and not attack_dict_variation and not attack_mask and not attack_bruteforce:
            return render_add_page("select at least one attack mode")

        # duration
        duration = int(request.form.get("duration", 3))

        if not request.form.get("confirm_btn", None):
            # render confirmation page if confirm button not sumblitted
            return render_add_page(confirmation=True, current_hashes=hashes)
        else:
            return jsonify({"message": "ok"})

    # render add crack page
    return render_add_page()
