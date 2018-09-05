# coding: utf8
import os

# third party imports
from flask import Blueprint, render_template, jsonify, request, flash
from flask_login import login_required

# local imports
from server import app
from app.forms.add_crack import AddCrackForm
from app.ref.hashes_list import HASHS_LIST
from app.helpers.files import FilesHelper
from app.helpers.crack import CrackHelper

from app.tasks.hashcat import launch_new_crack

cracks_post = Blueprint('cracks_post', __name__, template_folder='templates')


def get_filelist_checkbox_builder_dict(name, files_list):
    """
    function used to create a list of dictionary based on list of word files

    list returned is used in template to generate files checkboxes

    name parameter is either used to build file list for classic dict attack or for variation dict attack
    """
    result_files_list = []
    for f in files_list:
        sumbitted_values = request.form.get(name, None)
        result_files_list.append({
            'name': name,
            'label': f,
            'value': f,
            'checked': True if sumbitted_values and f in sumbitted_values else False
        })
    return result_files_list


def render_add_page(confirmation=False):
    """
    function used to render add template page
    """

    form = AddCrackForm(request.form)
    current_hashes = AddCrackForm.get_hashes()
    if current_hashes:
        form.hashes.data = current_hashes

    # render add form
    return render_template(
        'pages/add_crack.html',
        title="Add new crack" if not confirmation else "Confirm new crack",
        form=form,
        separator=app.config["HASHLIST_FILE_SEPARATOR"],
        hashes_list=HASHS_LIST,  # used to populate javascript function
        max_len=app.config["MAX_CONTENT_LENGTH"],
        wordlist_files_list=get_filelist_checkbox_builder_dict(
            'attack_classic_dict_files',
            FilesHelper.get_available_files(folder=app.config["APP_LOCATIONS"]["wordlists"])
        ),
        variations_files_list=get_filelist_checkbox_builder_dict(
            'attack_variations_dict_files',
            FilesHelper.get_available_files(folder=app.config["APP_LOCATIONS"]["rules"])
        ),
        confirmation=confirmation
    )


@cracks_post.route('/add', methods=["GET", "POST"])
@login_required
def add_new_crack():
    if request.method == "POST":

        # validate form content
        form_is_valid, messages = AddCrackForm.validate_custom()
        if not form_is_valid:
            for m in messages:
                if m:
                    flash(m, 'error')
            return render_add_page()

        # get hashes
        hashes = AddCrackForm.get_hashes()

        # get hashtype code
        hash_type_code = AddCrackForm.get_hash_type_code()

        # contains_usernames
        hashed_file_contains_usernames = AddCrackForm.get_file_contains_username()

        # attack_details
        attack_details = AddCrackForm.get_attack_details()

        # duration
        duration = AddCrackForm.get_duration()

        if not AddCrackForm.is_confirmation():
            # render confirmation page if confirm button not submitted
            return render_add_page(confirmation=True)
        else:
            output_file_path = os.path.join(
                app.config["APP_LOCATIONS"]["hashcat_outputs"],
                CrackHelper.get_output_file_name()
            )

            launch_new_crack.delay(
                hashes=hashes,
                hash_type_code=hash_type_code,
                output_file_path=output_file_path,
                hashed_file_contains_usernames=hashed_file_contains_usernames,
                duration=duration,
                attack_details=attack_details
            )

    # render add crack page on GET request
    return render_add_page()
