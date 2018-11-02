# coding: utf8
import os

# third party imports
from flask import flash, request
from flask_wtf import FlaskForm
from wtforms import TextAreaField, FileField, SelectField, BooleanField, RadioField, StringField, SubmitField, FormField, FieldList

# local imports
from server import app
from app.classes.Wordlist import Wordlist
from app.classes.Rule import Rule
from app.ref.hashes_list import HASHS_CODES_LIST
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
    for h in HASHS_CODES_LIST:
        rst.append((h["code"], h["name"]))
    return rst


class AddCrackRequestForm(FlaskForm):
    request_name = StringField("Request Name")
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

    rules = BooleanField("Use Rules (cusomise rules files in \"options\" tab if necessary)")

    bruteforce = BooleanField("Perform a bruteforce attack")

    duration = SelectField(
        "Select duration (days)",
        choices=get_durations_as_tuple()
    )

    use_potfile = BooleanField("Use potfile")

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
        hashes = AddCrackRequestForm.get_hashes()
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
        form.keywords.data = AddCrackRequestForm.get_keywords()

        return True

    @staticmethod
    def get_hash_type_code():
        return int(request.form.get("hash_type", 0))

    @staticmethod
    def get_file_contains_username():
        return request.form.get("hashed_file_contains_usernames", 'n') == 'y'

    @staticmethod
    def get_files_from_ref(obj_list, form_field, only_submited=False):
        if AddCrackRequestForm.is_submission():
            form_rules_files = request.form.getlist(form_field, None)
            updated_list = []
            for o in obj_list:
                app.logger.debug("Check if {} is in {}: {}".format(
                    o.filepath,
                    str(form_rules_files),
                    str(True if o.filepath in form_rules_files or o.filepath == form_rules_files else False)
                ))
                o.set_active(active=(True if o.filepath in form_rules_files else False))
                if not only_submited or (only_submited and o.active):
                    updated_list.append(o)

            return updated_list

        return obj_list

    @staticmethod
    def get_wordlists_files(only_submited=False):
        app.logger.debug("Get selected or default wordlists")
        return AddCrackRequestForm.get_files_from_ref(
            obj_list=Wordlist.get_all_from_config_and_ref_folder_as_instances(),
            form_field='wordlist_files',
            only_submited=only_submited
        )

    @staticmethod
    def get_mask():
        return request.form.get("mask", None)

    @staticmethod
    def get_rules():
        if request.form.get('rules', 'n') == 'y':
            return True
        return False

    @staticmethod
    def get_rules_files(only_submited=False):
        app.logger.debug("Get selected or default rules")
        return AddCrackRequestForm.get_files_from_ref(
            obj_list=Rule.get_all_from_config_and_ref_folder_as_instances(),
            form_field='rules_files',
            only_submited=only_submited
        )

    @staticmethod
    def get_bruteforce():
        if request.form.get('bruteforce', 'n') == 'y':
            return True
        return False

    @staticmethod
    def get_duration():
        return int(request.form.get("duration", 3))

    @staticmethod
    def get_use_potfile():
        if request.form.get('use_potfile', 'n') == 'y':
            return True
        return False

    @staticmethod
    def is_submission():
        """
        Validate that form was submitted
        :return:
        """
        return request.method == "POST"

    @staticmethod
    def is_confirmation():
        """
        Check that form is submitted and confirmation button was clicked
        :return:
        """
        return AddCrackRequestForm.is_submission() and request.form.get("confirm_btn", None)

    # custom validation method
    @staticmethod
    def validate_name(form):
        """
        Validate that request name is not empty
        :param form:
        :return:
        """
        if not request.form.get('request_name', None):
            return False, "Request name required"

        return True, ""

    @staticmethod
    def validate_hashes(form=None):
        """
        Validate that hashes is not empty
        :param form:
        :return:
        """
        if not AddCrackRequestForm.get_hashes(form):
            return False, "Hashes or hash file required"

        return True, ""

    @staticmethod
    def validate_hash_type_code():
        """
        Validate that provided hash type code is in ref list
        :return:
        """
        if not HashesHelper.validate_code(AddCrackRequestForm.get_hash_type_code()):
            return False, "Invalid hash code"

        return True, ""

    @staticmethod
    def validate_one_attack_selected(form=None):
        """
        method to check if an attack was selected, check if either one of :
            - one dict selected
            - keywords not empty
            - mask defined
            - bruteforce selected
        :param form: current form
        :return:
        """
        if not AddCrackRequestForm.get_wordlists_files(only_submited=True) \
                and not AddCrackRequestForm.get_keywords(form) \
                and not request.form.get('mask', None) \
                and not request.form.get('bruteforce', None):
            return False, "Select at least one attack type"
        app.logger.debug("An attack type was selected")
        if AddCrackRequestForm.get_wordlists_files(only_submited=True):
            app.logger.debug("An dict attack was selected")
            for f in AddCrackRequestForm.get_wordlists_files(only_submited=True):
                app.logger.debug("Selected dict: "+str(f.filepath_strict_name))
        return True, ""

    @staticmethod
    def validate_mask():
        """
        Check that mask format is respected
        :return:
        """
        mask = request.form.get('mask', None)
        if mask and not TextHelper.check_mask(mask):
            app.logger.debug("mask is invalid")
            return False, "Empty or invalid mask"

        return True, ""

    @staticmethod
    def validate_rules():
        if AddCrackRequestForm.get_rules() and not AddCrackRequestForm.get_rules_files(only_submited=True):
            return False, "To apply rules, select at least one rule in Options tab"
        return True, ""


    @staticmethod
    def validate_custom(form=None):
        """
        Validate that form contains at least:
            - name
            - hashes
            - hashes type
            - hash type code
            - an attack
        :param form:
        :return:
        """

        request_name_valid, name_message = AddCrackRequestForm.validate_name(form)
        hashes_valid, hashes_message = AddCrackRequestForm.validate_hashes(form)
        hashes_code_valid, hashes_code_message = AddCrackRequestForm.validate_hash_type_code()
        mask_valid, mask_message = AddCrackRequestForm.validate_mask()
        at_least_one_attack_selected, nb_attacks_message = AddCrackRequestForm.validate_one_attack_selected(form)
        valid_rules, rules_error_msg = AddCrackRequestForm.validate_rules()

        messages = [
            name_message,
            hashes_message,
            hashes_code_message,
            nb_attacks_message,
            mask_message,
            rules_error_msg
        ]

        if request_name_valid \
                or not hashes_valid \
                or not hashes_code_valid \
                or not at_least_one_attack_selected \
                or not mask_valid\
                or not valid_rules:
            return False, messages

        return True, []
