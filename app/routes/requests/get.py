# coding: utf8
# third party imports
from flask import Blueprint, render_template, jsonify, request, flash
from flask_login import login_required, current_user

# local imports
from server import db
from app.models.cracks.request import CrackRequest, CLOSE_MODES

requests_get = Blueprint('requests_get', __name__, template_folder='templates')


@requests_get.route('/requests', methods=["GET", "POST"])
@login_required
def get_all_user_request():
    print("fetch all requests for user id "+str(current_user.id))
    user_requests = CrackRequest.query.filter_by(user_id=current_user.id).all()

    print("render template")
    return render_template(
        'pages/requests.html',
        title="All your cracks",
        close_modes=CLOSE_MODES,
        user_requests=user_requests
    )
