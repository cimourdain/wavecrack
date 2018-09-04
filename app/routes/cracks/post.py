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
from app.helpers.rules import RulesHelper
from app.helpers.forms import FormHelper
from app.helpers.crack import CrackHelper

from app.tasks.hashcat import launch_new_crack

cracks_post = Blueprint('cracks_post', __name__, template_folder='templates')


def get_check_keywords_attack_details():
    result = None
    if request.form.get('attack_mode_keywords_cb', None):
        keywords = request.form.get('keywords', None)
        if not keywords:
            return render_add_page("Keywords list required")
        result = {"keywords": keywords}
    return result

def get_check_dict_attack_details():
    result = None
    if request.form.get('attack_mode_dict_classic_cb', None):
        # check at least one dict is selected
        attack_classic_dict_files = request.form.get('attack_classic_dict_files', None)
        if not attack_classic_dict_files:
            return render_add_page("List of dict required for classic dict attack")

        attack_variations_dict_files = request.form.get('attack_variations_dict_files', None)
        result = {
            "dict": {
                "files": attack_classic_dict_files,
                "variations": attack_variations_dict_files
            }
        }
    return result


def get_check_mask_attack_details():
    result = None
    if request.form.get('attack_mode_mask_cb', None):
        mask = request.form.get('mask', None)
        if not mask or not FormHelper.check_mask(mask):
            return render_add_page("Empty or invalid mask")
        result = {"mask": mask}

    return result

def get_check_bruteforce_attack_details():
    result = None
    if request.form.get('attack_mode_bruteforce_cb', None):
        result = {"bruteforce": True}
    return result

def get_check_attack_details():
    attack_details = []

    keyword_attack_details = get_check_keywords_attack_details()
    if keyword_attack_details:
        attack_details.append(keyword_attack_details)

    dict_attack_details = get_check_dict_attack_details()
    if dict_attack_details:
        attack_details.append(dict_attack_details)

    mask_attak_details = get_check_mask_attack_details()
    if mask_attak_details:
        attack_details.append(mask_attak_details)

    bruteforce_attack_details = get_check_bruteforce_attack_details()
    if bruteforce_attack_details:
        attack_details.append(bruteforce_attack_details)

    if not attack_details:
        return render_add_page("Choose at least one type of attack")

    return attack_details



def get_wordlists_cb(name, files_list):
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
        wordlist_files_list=get_wordlists_cb('attack_classic_dict_files', WordsHelper.get_available_wordlists()),
        variations_files_list=get_wordlists_cb('attack_variations_dict_files', RulesHelper.get_available_wordlists()),
        confirmation=confirmation
    )


@cracks_post.route('/add', methods=["GET", "POST"])
@login_required
def add_new_crack():
    if request.method == "POST" and FormHelper.check_fields_in_form(
            ["hashes", "hashes_file"]
    ):
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

        # attack_details
        attack_details = get_check_attack_details()

        # duration
        duration = int(request.form.get("duration", 3))

        if not request.form.get("confirm_btn", None):
            # render confirmation page if confirm button not submitted
            return render_add_page(confirmation=True, current_hashes=hashes)
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

    # render add crack page
    return render_add_page()
