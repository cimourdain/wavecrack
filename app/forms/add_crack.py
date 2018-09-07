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
from app.helpers.text import TextHelper


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

    keywords = TextAreaField("And/Or Enter keywords(one per line)", render_kw={
        "placeholder": "Enter keywords(one per line)"
    })
    keywords_file = FileField("And/Or upload keywords file")

    mask = TextAreaField("Enter masks(one per line)", render_kw={
        "placeholder": "Enter keywords(one per line)"
    })

    # note: rules generated manually

    bruteforce = BooleanField("Perform a bruteforce attack")

    duration = SelectField(
        "Select duration (days)",
        choices=get_durations_as_tuple()
    )

    submit_btn = SubmitField(label='Sumbit')
    confirm_btn = SubmitField(label='Confirm')

    """
    CUSTOM VALIDATION METHODS
    """
    @staticmethod
    def get_hashes(form=None):
        if form and form.hashes.data:
            return form.hashes.data

        if "hashes_file" in request.files and FormHelper.uploaded_file_is_valid("hashes_file", [".txt"]):
            return str(request.files["hashes_file"].read())

        return request.form.get("hashes", "")

    @staticmethod
    def set_hashes(form):
        hashes = AddCrackForm.get_hashes()
        form.hashes.data = hashes

        return True

    @staticmethod
    def get_keywords(form=None):
        if form and form.keywords.data:
            return form.keywords.data

        if "keywords_file" in request.files and FormHelper.uploaded_file_is_valid("keywords_file", [".txt"]):
            return str(request.files["keywords_file"].read())

        return request.form.get("keywords", "")

    @staticmethod
    def set_keywords(form):
        form.keywords.data = AddCrackForm.get_keywords()

        return True

    @staticmethod
    def get_hash_type_code():
        return int(request.form.get("hash_type", 0))

    @staticmethod
    def get_file_contains_username():
        return request.form.get("hashed_file_contains_usernames", 'n')

    @staticmethod
    def get_wordlists_files():
        return request.form.get('wordlist_files', None)

    @staticmethod
    def get_mask():
        return request.form.get("mask", None)

    @staticmethod
    def get_rules_files():
        return request.form.get('rules_files', None)

    @staticmethod
    def get_bruteforce():
        if request.form.get('bruteforce', 'n') == 'y':
            return 1
        return 0

    @staticmethod
    def get_duration():
        return int(request.form.get("duration", 3))

    @staticmethod
    def is_confirmation():
        return request.form.get("confirm_btn", None)

    # custom validation method
    @staticmethod
    def validate_hashes(form=None):
        if not AddCrackForm.get_hashes(form):
            return False, "Hashes or hash file required"

        return True, ""

    @staticmethod
    def validate_hash_type_code():
        if not HashesHelper.validate_code(AddCrackForm.get_hash_type_code()):
            return False, "Invalid hash code"

        return True, ""

    @staticmethod
    def validate_one_attack_selected(form=None):
        if not AddCrackForm.get_wordlists_files() \
                and not AddCrackForm.get_keywords(form) \
                and not request.form.get('mask', None) \
                and not request.form.get('bruteforce', None):

            return False, "Select at least one attack type"
        return True, ""

    @staticmethod
    def validate_mask():
        mask = request.form.get('mask', None)
        if mask and not TextHelper.check_mask(mask):
            return False, "Empty or invalid mask"

        return True, ""

    @staticmethod
    def validate_custom(form=None):
        hashes_valid, hashes_message = AddCrackForm.validate_hashes(form)
        hashes_code_valid, hashes_code_message = AddCrackForm.validate_hash_type_code()
        mask_valid, mask_message = AddCrackForm.validate_mask()

        at_least_one_attack_selected, nb_attacks_message = AddCrackForm.validate_one_attack_selected(form)

        messages = [
            hashes_message,
            hashes_code_message,
            nb_attacks_message,
            mask_message
        ]

        if not hashes_valid \
                or not hashes_code_valid \
                or not at_least_one_attack_selected \
                or not mask_valid:
            return False, messages

        return True, []





