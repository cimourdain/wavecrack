# coding: utf8
import os

# third party imports
from flask import Blueprint, render_template, jsonify
from flask_login import login_required

# local imports
from server import app
from app.helpers.hashes import HashesHelper
from app.helpers.words import WordsHelper

cracks_post = Blueprint('cracks_post', __name__, template_folder='templates')


@cracks_post.route('/add/validate', methods=["POST"])
@login_required
def validate_new_crack():
    pass
