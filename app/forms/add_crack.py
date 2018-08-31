import os

# third party imports
from flask import flash
from flask_wtf import FlaskForm
from wtforms import TextAreaField, FileField, SelectField, BooleanField, RadioField, StringField, SubmitField

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


class WordListCheckBox(FlaskForm):
    wordlist_file = BooleanField(default="checked")


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

    wordlist_attack_type = RadioField("attack type", choices=[
        ("0", "Classic wordlist attack"),
        ("1", "Wordlist attack with variations"),
        ("2", "Mask"),
        ("3", "Keywords"),
        ("4", "BruteForce")
    ])

    keywords = TextAreaField("Enter keyword(s) (one per line)", render_kw={
        "placeholder": "Enter keyword(s) (one per line)"
    })

    mask = StringField("Mask", render_kw={
        "placeholder": "Enter the mask"
    })

    duration = SelectField(
        "Select duration (days)",
        choices=get_durations_as_tuple()
    )

    submit_btn = SubmitField(label='Sumbit')
