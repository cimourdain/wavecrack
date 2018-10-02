# coding: utf8
# standard imports
import os

# third party imports
from flask import Blueprint, render_template, jsonify, request, flash, redirect, url_for
from flask_login import login_required
import psutil

server_get = Blueprint('server_get', __name__, template_folder='templates')


@server_get.route('/server', methods=["GET"])
@login_required
def server_load():
    pass