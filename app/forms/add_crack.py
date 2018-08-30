
# third party imports
from flask_wtf import FlaskForm
from wtforms import TextAreaField, FileField, SelectField, BooleanField

# local imports
from server import app
from app.ref.hashes_list import HASHS_LIST


def get_hashes_list_as_tuples():
    rst = []
    for h in HASHS_LIST:
        rst.append((h["code"], h["name"]))
    return rst


class AddCrackForm(FlaskForm):
    hashes = TextAreaField("Enter the hash list (one per line)", render_kw={
        "placeholder": "Enter the hash list (one per line)"
    })
    hashes_file = FileField("Upload file with hashes")
    hashed_file_contains_usernames = BooleanField("The hash list contains usernames")
    hash_type = SelectField(
        "Select the hash type.",
        choices=get_hashes_list_as_tuples(),
        render_kw={
            "onChange": "UpdateHashExample()"
        }
    )
    keywords = BooleanField("Keyword(s)")
    wordlist_attack = BooleanField("Wordlist attack")
    chosen_keywords = TextAreaField("Enter keyword(s) (one per line)", render_kw={
        "placeholder": "Enter keyword(s) (one per line)"
    })


