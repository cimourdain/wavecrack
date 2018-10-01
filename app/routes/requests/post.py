# coding: utf8
import os

# third party imports
from flask import Blueprint, render_template, jsonify, request, flash, redirect, url_for
from flask_login import login_required

# local imports
from server import app
from app.forms.add_request import AddCrackRequestForm
from app.ref.hashes_list import HASHS_LIST
from app.helpers.files import FilesHelper
from flask_login import current_user

from app.tasks.hashcat import launch_new_crack_request

requests_post = Blueprint('requests_post', __name__, template_folder='templates')


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
            'label': os.path.splitext(os.path.basename(f))[0],
            'value': f,
            'checked': True if sumbitted_values and f in sumbitted_values else False
        })
    return result_files_list


def render_add_page(form, confirmation=False):
    """
    function used to render add template page
    """

    # render add form
    return render_template(
        'pages/requests/request_add.html',
        title="Add new crack request" if not confirmation else "Confirm new crack request",
        form=form,
        separator=app.config["HASHLIST_FILE_SEPARATOR"],
        hashes_list=HASHS_LIST,  # used to populate javascript function
        max_len=app.config["MAX_CONTENT_LENGTH"],
        wordlist_files_list=get_filelist_checkbox_builder_dict(
            'wordlist_files',
            FilesHelper.get_available_files(folder=app.config["DIR_LOCATIONS"]["wordlists"])
        ),
        rules_files_list=get_filelist_checkbox_builder_dict(
            'rules_files',
            FilesHelper.get_available_files(folder=app.config["DIR_LOCATIONS"]["rules"])
        ),
        confirmation=confirmation
    )


@requests_post.route('/add', methods=["GET", "POST"])
@login_required
def add_new_crack_request():
    form = AddCrackRequestForm(request.form)

    if request.method == "POST":
        # set hashes from file content to hashes textarea if required
        AddCrackRequestForm.set_hashes(form)
        AddCrackRequestForm.set_keywords(form)

        # validate form content
        form_is_valid, messages = AddCrackRequestForm.validate_custom(form)
        if not form_is_valid:
            for m in messages:
                if m:
                    flash(m, 'error')
            return render_add_page(form)

        # get hashes
        hashes = AddCrackRequestForm.get_hashes()

        # get hashtype code
        hash_type_code = AddCrackRequestForm.get_hash_type_code()

        # contains_usernames
        hashed_file_contains_usernames = AddCrackRequestForm.get_file_contains_username()


        wordlist_files = AddCrackRequestForm.get_wordlists_files()
        keywords = AddCrackRequestForm.get_keywords()
        mask = AddCrackRequestForm.get_mask()
        rules = AddCrackRequestForm.get_rules_files()
        bruteforce = AddCrackRequestForm.get_bruteforce()

        # duration
        duration = AddCrackRequestForm.get_duration()

        if not AddCrackRequestForm.is_confirmation():
            # render confirmation page if confirm button not submitted
            return render_add_page(form=form, confirmation=True)
        else:

            launch_new_crack_request.delay(
                name=form.request_name.data,
                user_id=current_user.id,
                hashes=hashes,
                hashes_type_code=hash_type_code,
                hashed_file_contains_usernames=hashed_file_contains_usernames,
                duration=duration,
                wordlist_files=wordlist_files,
                keywords=keywords,
                mask=mask,
                rules=rules,
                bruteforce=bruteforce
            )
            return redirect(url_for('requests_get.get_all_user_request'))

    # render add crack page on GET request
    return render_add_page(form=form)


