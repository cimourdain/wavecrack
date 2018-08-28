# coding: utf8
import os

# third party imports
from flask import Blueprint, render_template, jsonify
from flask_login import login_required

# local imports
from server import app

user_get = Blueprint('user_get', __name__, template_folder='templates')


@user_get.route('/login', methods=["GET"])
def login():
    return jsonify({"welcome": "login page"})
