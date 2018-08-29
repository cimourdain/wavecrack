# coding: utf8
import os

# third party imports
from flask import Blueprint, render_template, jsonify
from flask_login import login_required

# local imports
from server import app
from app.helpers.hashes import HashesHelper
from app.helpers.words import WordsHelper

cracks_get = Blueprint('cracks_get', __name__, template_folder='templates')


@cracks_get.route('/add', methods=["GET"])
@login_required
def add_new_crack():
    return render_template(
        'cracks/add.html',
        title="Add new crack",
        HASHS_LIST=HashesHelper.HASHS_LIST,
        wordlist_languages=WordsHelper.get_available_languages(),
        separator=app.config["HASHLIST_OUTFILE_SEPARATOR"],
        max_size=app.config['MAX_CONTENT_LENGTH'],
        CRACK_DURATIONS=app.config["CRACK_DURATIONS"]
    )
