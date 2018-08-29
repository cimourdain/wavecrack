# coding: utf8

# third party imports
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user

# local imports
from app.models.user import User

user_post = Blueprint('user_post', __name__, template_folder='templates')


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
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for('home_get.render_homepage')
            return redirect(next)

    # define login message if form submitted
    if request.method == "POST":
        flash('Invalid login', 'error')

    # render login page
    return render_template(
        'auth/login.html',
        title="Login",
        login_message=login_message
    )