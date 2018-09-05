import os

# third party imports
from flask import flash, request
from flask_wtf import FlaskForm
from wtforms import TextAreaField, FileField, SelectField, BooleanField, RadioField, StringField, SubmitField, FormField, FieldList

# local imports
from server import app
from app.ref.hashes_list import HASHS_LIST
from app.helpers.forms import FormHelper
from app.helpers.hashes import HashesHelper


def get_durations_as_tuple():
    duration_tuples = []
    for d in app.config["CRACK_DURATIONS"]:
        duration_tuples.append((str(d), str(d)))

    return duration_tuples


def get_hashes_list_as_tuples():
    rst = []
    for h in HASHS_LIST:
        rst.append((h["code"], h["name"]))
    return rst


class AddCrackForm(FlaskForm):
    hashes = TextAreaField("Enter the hash list (one per line)",render_kw={
        "placeholder": "Enter the hash list (one per line)"
    })
    hashes_file = FileField("Upload file with hashes")
    hashed_file_contains_usernames = BooleanField("The hash file contains usernames")
    hash_type = SelectField(
        "Select the hash type.",
        choices=get_hashes_list_as_tuples(),
        render_kw={
            "onChange": "UpdateHashExample()"
        }
    )

    attack_mode_keywords_cb = BooleanField("Keywords")
    keywords = TextAreaField("Enter keyword(s) (one per line)", render_kw={
        "placeholder": "Enter keyword(s) (one per line)"
    })

    attack_mode_dict_classic_cb = BooleanField("Classic dictionnary")
    attack_mode_dict_variations_cb = BooleanField("Dictionnary with variations")

    attack_mode_mask_cb = BooleanField("Mask")
    mask = StringField("Mask", render_kw={
        "placeholder": "Enter the mask"
    })

    attack_mode_bruteforce_cb = BooleanField("Bruteforce")

    duration = SelectField(
        "Select duration (days)",
        choices=get_durations_as_tuple()
    )

    submit_btn = SubmitField(label='Sumbit')
    confirm_btn = SubmitField(label='Confirm')

    # custom get method
    @staticmethod
    def get_hashes():
        hashes = request.form.get("hashes", "")
        if "hashes_file" in request.files and FormHelper.uploaded_file_is_valid("hashes_file", [".txt"]):
            hashes = request.files["hashes_file"].read()

        return hashes

    @staticmethod
    def get_hash_type_code():
        return int(request.form.get("hash_type", 0))

    @staticmethod
    def get_file_contains_username():
        return request.form.get("hashed_file_contains_usernames", 'n')

    @staticmethod
    def get_duration():
        return int(request.form.get("duration", 3))

    @staticmethod
    def is_confirmation():
        return request.form.get("confirm_btn", None)

    # custom validation method
    @staticmethod
    def validate_hashes():
        if not AddCrackForm.get_hashes():
            return False, "Hashes or hash file required"

        return True, ""

    @staticmethod
    def validate_hash_type_code():
        if not HashesHelper.validate_code(AddCrackForm.get_hash_type_code()):
            return False, "Invalid hash code"

        return True, ""

    @staticmethod
    def validate_one_attack_selected():
        if not request.form.get('attack_mode_keywords_cb', None) \
                and not request.form.get('attack_mode_dict_classic_cb', None) \
                and not request.form.get('attack_mode_mask_cb', None) \
                and not request.form.get('attack_mode_bruteforce_cb', None):
            print("Not one attack mode selected")
            return False, "Select at least one attack type"
        return True, ""

    @staticmethod
    def validate_keywords():
        if request.form.get('attack_mode_keywords_cb', None):
            keywords = request.form.get('keywords', None)
            if not keywords:
                return False, "keywords required for a keyword attack"

        return True, ""

    @staticmethod
    def validate_dict_attack():
        if request.form.get('attack_mode_dict_classic_cb', None):
            # check at least one dict is selected
            if not request.form.get('attack_classic_dict_files', None):
                return False, "List of dict required for classic dict attack"

        return True, ""

    @staticmethod
    def validate_mask():
        if request.form.get('attack_mode_mask_cb', None):
            mask = request.form.get('mask', None)
            if not mask or not FormHelper.check_mask(mask):
                return False, "Empty or invalid mask"

        return True, ""

    @staticmethod
    def validate_custom():
        hashes_valid, hashes_message = AddCrackForm.validate_hashes()
        hashes_code_valid, hashes_code_message = AddCrackForm.validate_hash_type_code()
        keywords_valid, keywords_message = AddCrackForm.validate_keywords()
        dict_valid, dict_message = AddCrackForm.validate_dict_attack()
        mask_valid, mask_message = AddCrackForm.validate_mask()

        at_least_one_attack_selected, nb_attacks_message = AddCrackForm.validate_one_attack_selected()

        messages = [
            hashes_message,
            hashes_code_message,
            nb_attacks_message,
            keywords_message,
            dict_message,
            mask_message
        ]

        if not hashes_valid \
                or not hashes_code_valid \
                or not at_least_one_attack_selected \
                or not keywords_valid \
                or not dict_valid or not mask_valid:
            return False, messages

        return True, []

    """
    Custom methods to build a dictionary with attack details
    """
    @staticmethod
    def get_keywords_attack_details():
        if request.form.get('attack_mode_keywords_cb', None):
            keywords = request.form.get('keywords', None)
            return {"keywords": keywords}
        return None

    @staticmethod
    def get_dict_attack_details():
        if request.form.get('attack_mode_dict_classic_cb', None):
            # check at least one dict is selected
            attack_classic_dict_files = request.form.get('attack_classic_dict_files', None)
            attack_variations_dict_files = request.form.get('attack_variations_dict_files', None)
            return {
                "dict": {
                    "files": attack_classic_dict_files,
                    "variations": attack_variations_dict_files
                }
            }
        return None

    @staticmethod
    def get_mask_attack_details():
        if request.form.get('attack_mode_mask_cb', None):
            mask = request.form.get('mask', None)
            return {"mask": mask}

        return None

    @staticmethod
    def get_bruteforce_attack_details():
        if request.form.get('attack_mode_bruteforce_cb', None):
            return {"bruteforce": True}
        return None

    @staticmethod
    def get_attack_details():
        attack_details = []

        keyword_attack_details = AddCrackForm.get_keywords_attack_details()
        if keyword_attack_details:
            attack_details.append(keyword_attack_details)

        dict_attack_details = AddCrackForm.get_dict_attack_details()
        if dict_attack_details:
            attack_details.append(dict_attack_details)

        mask_attak_details = AddCrackForm.get_mask_attack_details()
        if mask_attak_details:
            attack_details.append(mask_attak_details)

        bruteforce_attack_details = AddCrackForm.get_bruteforce_attack_details()
        if bruteforce_attack_details:
            attack_details.append(bruteforce_attack_details)

        return attack_details





