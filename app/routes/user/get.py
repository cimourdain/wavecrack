# coding: utf8

# third party imports
from flask import Blueprint, flash, url_for, render_template
from flask_login import logout_user, login_required

user_get = Blueprint('user_get', __name__, template_folder='templates')


@user_get.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logout successful', 'success')
    return render_template(
        'homepage.html',
        title="Homepage"
    )
