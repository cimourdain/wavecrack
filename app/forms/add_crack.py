import os

# third party imports
from flask import flash
from flask_wtf import FlaskForm
from wtforms import TextAreaField, FileField, SelectField, BooleanField, RadioField, StringField, SubmitField, FormField, FieldList

# local imports
from server import app
from app.ref.hashes_list import HASHS_LIST


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
