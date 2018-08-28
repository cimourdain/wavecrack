# coding: utf8
import os

# third party imports
from flask import Blueprint, render_template, jsonify
from flask_login import login_required

# local imports
from server import app

user_post = Blueprint('user_post', __name__, template_folder='templates')


@user_post.route('/login', methods=["POST"])
def login():
    pass