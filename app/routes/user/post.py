# coding: utf8

# third party imports
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user

# local imports
from app.models.user import User

user_post = Blueprint('user_post', __name__, template_folder='templates')


def get_page_to_redirect():
    next = request.args.get('next', None)
    if not next or not next.startswith('/') or next.find("logout") != -1:
        next = url_for('home_get.render_homepage')
    return redirect(next)


@user_post.route('/login', methods=["GET", "POST"])
def login():
    login_message = ""

    # check login/password if form submitted
    if "login" in request.form and "password" in request.form:
        # find user with login matching either email or name
        user = User.get_user(login=request.form["login"])

        # check password
        if user is not None and user.verify_password(request.form["password"]):

            # remember user if checkbox activated
            remember_user = True if "remember_me" in request.form and request.form["remember_me"] in [1, "1"] else False
            login_user(user, remember_user)

            # redirect user
            return get_page_to_redirect()

    # define login message if form submitted
    if request.method == "POST":
        flash('Invalid login', 'error')

    # render login page
    return redirect(url_for('home_get.render_homepage'))
