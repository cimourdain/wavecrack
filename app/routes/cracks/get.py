# coding: utf8

# third party imports
from flask import Blueprint, render_template, jsonify, request, flash, send_from_directory
from flask_login import login_required, current_user

# local imports
from server import db
from app.models.cracks.request import CrackRequest, REQUESTS_CLOSE_MODES
from app.models.cracks.entity import Crack
from app.helpers.files import FilesHelper

cracks_get = Blueprint('cracks_get', __name__, template_folder='templates')


def get_crack(crack_id):
    try:
        crack = Crack.query.filter_by(id=crack_id).one()
    except Exception as _:
        flash("Error: crack not found", "error")
        return render_template('pages/home.html', title="crack not found")

    if crack.request.user.id != current_user.id and not current_user.is_admin:
        flash("Error: invalid access", "error")
        return render_template('pages/home.html', title="crack not found")

    return crack


@cracks_get.route('/cracks/<crack_id>/output_file', methods=["GET"])
@login_required
def download_crack_outfile(crack_id):

    crack = get_crack(crack_id)

    folder_path, filename = FilesHelper.split_path(crack.output_file_path)
    return send_from_directory(directory=folder_path, filename=filename)


@cracks_get.route('/cracks/<crack_id>/potfile', methods=["GET"])
@login_required
def download_crack_potfile(crack_id):

    crack = get_crack(crack_id)

    folder_path, filename = FilesHelper.split_path(crack.potfile_path)
    return send_from_directory(directory=folder_path, filename=filename)


@cracks_get.route('/cracks/<crack_id>/cmd_output_file', methods=["GET"])
@login_required
def download_crack_cmd_outfile(crack_id):
    crack = get_crack(crack_id)

    folder_path, filename = FilesHelper.split_path(crack.output_file_path)

    return send_from_directory(directory=folder_path, filename="cmd_output.txt")


@cracks_get.route('/cracks/<crack_id>/cmd_error_file', methods=["GET"])
@login_required
def download_crack_cmd_errfile(crack_id):
    crack = get_crack(crack_id)

    folder_path, filename = FilesHelper.split_path(crack.output_file_path)

    return send_from_directory(directory=folder_path, filename="cmd_err.txt")

