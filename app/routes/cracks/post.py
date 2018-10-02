# coding: utf8

# third party imports
from flask import Blueprint, render_template, jsonify, request, flash, redirect, url_for
from flask_login import login_required

# local imports
from server import app
from app.models.cracks.entity import Crack


cracks_post = Blueprint('cracks_post', __name__, template_folder='templates')


@cracks_post.route('/kill_crack/<crack_id>', methods=["GET", "POST"])
@login_required
def kill_crack(crack_id):
    try:
        crack = Crack.query.filter_by(id=crack_id).one()
    except Exception as _:
        flash("Error: crack not found", "error")
        return render_template('pages/home.html', title="crack not found")

    crack.force_close()

    return redirect(url_for('requests_get.get_unique_request', request_id=crack.request.id))
