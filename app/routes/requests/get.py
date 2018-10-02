# coding: utf8

# third party imports
from flask import Blueprint, render_template, jsonify, request, flash, send_from_directory
from flask_login import login_required, current_user

# local imports
from server import db
from app.models.cracks.request import CrackRequest, REQUESTS_CLOSE_MODES
from app.models.cracks.entity import Crack
from app.helpers.files import FilesHelper

requests_get = Blueprint('requests_get', __name__, template_folder='templates')


@requests_get.route('/requests', methods=["GET"])
@login_required
def get_all_user_request():
    user_requests = CrackRequest.query.filter_by(user_id=current_user.id).all()

    print("render template")
    return render_template(
        'pages/requests/requests_list.html',
        title="All your cracks",
        close_modes=REQUESTS_CLOSE_MODES,
        user_requests=user_requests
    )


@requests_get.route('/requests/<request_id>', methods=["GET"])
@login_required
def get_unique_request(request_id):
    # fetch crack request
    try:
        request = CrackRequest.query.filter_by(user_id=current_user.id, id=request_id).one()
    except Exception as _:
        flash("Error: request not found", "error")
        return render_template('pages/home.html', title="request not found")

    if request.is_archived:
        flash("request is archived", "info")

    return render_template(
        'pages/requests/request_detail.html',
        title="Request detail: "+request.name,
        request=request
    )


@requests_get.route('/requests/<request_id>/input_file', methods=["GET"])
@login_required
def download_original_password_file(request_id):
    try:
        request = CrackRequest.query.filter_by(user_id=current_user.id, id=request_id).one()
    except Exception as _:
        flash("Error: request not found", "error")
        return render_template('pages/home.html', title="request not found")

    folder_path, filename = FilesHelper.split_path(request.hashes_path)
    return send_from_directory(directory=folder_path, filename=filename)


@requests_get.route('/requests/<request_id>/output_file', methods=["GET"])
@login_required
def download_output_file(request_id):
    try:
        request = CrackRequest.query.filter_by(user_id=current_user.id, id=request_id).one()
    except Exception as _:
        flash("Error: request not found", "error")
        return render_template('pages/home.html', title="request not found")

    folder_path, filename = FilesHelper.split_path(request.outfile_path)
    return send_from_directory(directory=folder_path, filename=filename)
