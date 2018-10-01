# coding: utf8

# third party imports
from flask import Blueprint, render_template, jsonify, request, flash, redirect, url_for
from flask_login import login_required

# local imports
from server import app


cracks_post = Blueprint('cracks_post', __name__, template_folder='templates')


@cracks_post.route('/trregfd', methods=["GET", "POST"])
@login_required
def kill_crack():
    pass


