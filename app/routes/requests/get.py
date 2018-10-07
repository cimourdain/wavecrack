# coding: utf8

# third party imports
from flask import Blueprint, render_template, flash, send_from_directory
from flask_login import login_required, current_user

# local imports
from server import app
from app.models.cracks.request import CrackRequest, REQUESTS_CLOSE_MODES
from app.helpers.files import FilesHelper

requests_get = Blueprint('requests_get', __name__, template_folder='templates')


def get_request(request_id):
    if current_user.is_admin:
        return CrackRequest.query.filter_by(id=request_id).one()
    else:
        return CrackRequest.query.filter_by(user_id=current_user.id, id=request_id).one()


@requests_get.route('/user_requests', defaults={'user_id': current_user.id if current_user else ""}, methods=["GET"])
@requests_get.route('/user_requests/<user_id>', methods=["GET"])
@login_required
def get_all_user_request(user_id):
    """
    Route used to render all user crack request
    By default, route render current user request
    Only admins can view other users requests

    :param user_id:
    :return:
    """
    app.logger.debug("Enter user_requests route")
    if current_user.is_admin:
        user_requests = CrackRequest.query.filter_by(user_id=user_id).order_by(CrackRequest.start_date.desc()).all()
    else:
        user_requests = CrackRequest.query.filter_by(user_id=current_user.id).order_by(
            CrackRequest.start_date.desc()).all()

    user_requests = [x for x in user_requests if not x.is_archived]

    return render_template(
        'pages/requests/requests_list.html',
        title="All your cracks",
        close_modes=REQUESTS_CLOSE_MODES,
        user_requests=user_requests
    )


@requests_get.route('/all_requests', methods=["GET"])
@login_required
def get_all_requests():
    if not current_user.is_admin:
        return render_template('pages/home.html', title="home")

    all_requests = CrackRequest.query.order_by(CrackRequest.start_date.desc()).all()
    all_requests = [x for x in all_requests if not x.is_archived]

    return render_template(
        'pages/requests/requests_list.html',
        title="All your cracks",
        close_modes=REQUESTS_CLOSE_MODES,
        user_requests=all_requests
    )

@requests_get.route('/requests/<request_id>', methods=["GET"])
@login_required
def get_unique_request(request_id):
    """
    Route used to render request details

    :param request_id:
    :return:
    """
    # fetch crack request
    try:
        request = get_request(request_id)
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
    """
    Route to download crack request hash file

    :param request_id:
    :return:
    """
    try:
        request = get_request(request_id)
    except Exception as _:
        flash("Error: request not found", "error")
        return render_template('pages/home.html', title="request not found")

    folder_path, filename = FilesHelper.split_path(request.hashes_path)
    return send_from_directory(directory=folder_path, filename=filename)


@requests_get.route('/requests/<request_id>/output_file', methods=["GET"])
@login_required
def download_output_file(request_id):
    """
    Route to download request output file

    :param request_id:
    :return:
    """
    try:
        request = get_request(request_id)
    except Exception as _:
        flash("Error: request not found", "error")
        return render_template('pages/home.html', title="request not found")

    folder_path, filename = FilesHelper.split_path(request.outfile_path)
    return send_from_directory(directory=folder_path, filename=filename)


@requests_get.route('/requests/<request_id>/mask', methods=["GET"])
@login_required
def download_mask_file(request_id):
    try:
        request = get_request(request_id)
    except Exception as _:
        flash("Error: request not found", "error")
        return render_template('pages/home.html', title="request not found")

    folder_path, filename = FilesHelper.split_path(request.mask_path)
    return send_from_directory(directory=folder_path, filename=filename)
