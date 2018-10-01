# coding: utf8

# third party imports
from flask import Blueprint, render_template, jsonify, request, flash, send_from_directory
from flask_login import login_required, current_user

# local imports
from server import db
from app.models.cracks.request import CrackRequest, CLOSE_MODES
from app.models.cracks.entity import Crack
from app.helpers.files import FilesHelper

cracks_get = Blueprint('cracks_get', __name__, template_folder='templates')


@cracks_get.route('/cracks/<crack_id>/output_file', methods=["GET"])
@login_required
def download_crack_outfile(crack_id):
    try:
        crack = Crack.query.filter_by(id=crack_id).one()
    except Exception as _:
        flash("Error: crack not found", "error")
        return render_template('pages/home.html', title="crack not found")

    if crack.request.user.id != current_user.id:
        flash("Error: crack not found", "error")
        return render_template('pages/home.html', title="crack not found")

    folder_path, filename = FilesHelper.split_path(crack.output_file_path)
    return send_from_directory(directory=folder_path, filename=filename)

