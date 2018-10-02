# coding: utf8

# third party imports
from flask import Blueprint, render_template, jsonify, request, flash, redirect, url_for
from flask_login import login_required
import psutil

# local imports
from app.classes.cmd import Cmd
from app.models.cracks.entity import Crack

server_get = Blueprint('server_get', __name__, template_folder='templates')


@server_get.route('/server', methods=["GET"])
@login_required
def server_load():
    nb_cpu = psutil.cpu_count()
    cpu_load = psutil.cpu_percent(interval=1, percpu=True)
    memory = psutil.virtual_memory()

    # fetch all haschat instances
    haschat_pids = Cmd.get_process_pids("hashcat")
    haschat_pids = [] if not haschat_pids else haschat_pids[:-1].split(" ")

    running_cracks = Crack.query.filter(Crack.process_id.in_(haschat_pids)).all()

    return render_template(
        'pages/server.html',
        title="Server Admin",
        nb_cpu=nb_cpu,
        cpu_load=cpu_load,
        memory=memory,
        running_cracks=running_cracks
    )
