# coding: utf8
import os

# third party imports
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required

# local imports
from server import app, db
from app.forms.add_request import AddCrackRequestForm
from app.ref.hashes_list import HASHS_LIST
from app.helpers.files import FilesHelper
from flask_login import current_user

from app.models.cracks.request import CrackRequest
from app.tasks.hashcat import launch_new_crack_request
from app.routes.requests.get import get_request

requests_post = Blueprint('requests_post', __name__, template_folder='templates')


def create_new_crack_request(name, user_id, hashes, hashes_type_code,
                             hashed_file_contains_usernames, duration, wordlists=None,
                             keywords=None, mask=None, rules=None, bruteforce=None, use_potfile=False):

    app.logger.debug("requests_post :: create_new_crack_request")
    new_crack_request = CrackRequest()
    new_crack_request.user_id = user_id
    new_crack_request.name = name
    new_crack_request.hashes_type_code = hashes_type_code
    db.session.add(new_crack_request)
    db.session.flush()

    new_crack_request.init_request_folder()

    new_crack_request.duration = duration
    new_crack_request.use_potfile = use_potfile

    new_crack_request.hashed_file_contains_usernames = hashed_file_contains_usernames
    new_crack_request.hashes = hashes

    for wl in wordlists:
        new_crack_request.add_dictionary_paths(wordlists)

    if keywords:
        new_crack_request.keywords = keywords

    if mask:
        new_crack_request.mask = mask

    if rules:
        new_crack_request.add_rules(rules)

    new_crack_request.bruteforce = bruteforce

    app.logger.debug("requests_post :: create_new_crack_request :: add & save")

    db.session.flush()

    return new_crack_request


def render_add_page(form, confirmation=False):
    """
    function used to render add template page
    """

    # render add form
    app.logger.debug("requests_post :: render_add_page")
    return render_template(
        'pages/requests/request_add.html',
        title="Add new crack request" if not confirmation else "Confirm new crack request",
        form=form,
        separator=app.config["HASHLIST_FILE_SEPARATOR"],
        hashes_list=HASHS_LIST,  # used to populate javascript function
        max_len=app.config["MAX_CONTENT_LENGTH"],
        wordlist_files_list=form.get_wordlists_files(),
        rules_files_list=form.get_rules_files(),
        confirmation=confirmation
    )


@requests_post.route('/add', methods=["GET", "POST"])
@login_required
def add_new_crack_request():
    app.logger.debug("requests_post :: add_new_crack_request :: init form")
    form = AddCrackRequestForm(request.form)

    if request.method == "POST":
        # set hashes from file content to hashes textarea if required
        app.logger.debug("requests_post :: add_new_crack_request :: set hashes from file content")
        AddCrackRequestForm.set_hashes(form)
        app.logger.debug("requests_post :: add_new_crack_request :: set keywords from file content")
        AddCrackRequestForm.set_keywords(form)

        # validate form content
        app.logger.debug("requests_post :: add_new_crack_request :: validate form content")
        form_is_valid, messages = AddCrackRequestForm.validate_custom(form)
        if not form_is_valid:
            for m in messages:
                if m:
                    flash(m, 'error')
            return render_add_page(form)

        # extract elements from form data
        app.logger.debug("requests_post :: add_new_crack_request :: extract elements from form data")

        if not AddCrackRequestForm.is_confirmation():
            # render confirmation page if confirm button not submitted
            app.logger.debug("requests_post :: add_new_crack_request :: render confirmation page")
            return render_add_page(form=form, confirmation=True)
        else:
            # create new crack request
            app.logger.debug("requests_post :: add_new_crack_request :: create new crack request")
            new_crack_request = create_new_crack_request(
                name=form.request_name.data,
                user_id=current_user.id,
                hashes=AddCrackRequestForm.get_hashes(),
                hashes_type_code=AddCrackRequestForm.get_hash_type_code(),
                hashed_file_contains_usernames=AddCrackRequestForm.get_file_contains_username(),
                duration=AddCrackRequestForm.get_duration(),
                wordlists=AddCrackRequestForm.get_wordlists_files(only_submited=True),
                keywords=AddCrackRequestForm.get_keywords(),
                mask=AddCrackRequestForm.get_mask(),
                rules=AddCrackRequestForm.get_rules_files(only_submited=True) if AddCrackRequestForm.get_rules() else None,
                bruteforce=AddCrackRequestForm.get_bruteforce(),
                use_potfile=AddCrackRequestForm.get_use_potfile()
            )

            # build cracks for request
            app.logger.debug("requests_post :: add_new_crack_request :: build cracks for request")
            new_crack_request.prepare_cracks()

            # launch request cracks
            app.logger.debug("requests_post :: add_new_crack_request :: launch cracks (via celery task)")
            launch_new_crack_request.delay(
                crack_request_id=new_crack_request.id
            )

            # render list of requests
            app.logger.debug("requests_post :: add_new_crack_request :: render list of requests")
            return redirect(url_for('requests_get.get_all_user_request'))

    # render add crack page on GET request
    return render_add_page(form=form)


@requests_post.route('/kill_all_cracks/<request_id>', methods=["POST"])
@login_required
def kill_all_cracks_in_request(request_id):
    # load request
    try:
        request = get_request(request_id)
    except Exception as _:
        flash("Error: request not found", "error")
        return render_template('pages/home.html', title="request not found")

    # close all cracks
    if request and not request.is_archived:
        for crack in request.cracks:
            crack.force_close()

    # render request page details
    return redirect(url_for('requests_get.get_unique_request', request_id=request_id))


@requests_post.route('/request/delete/<request_id>', methods=["POST"])
@login_required
def delete_request(request_id):
    request = get_request(request_id)

    if request:
        FilesHelper.delete_directory(request.request_working_folder)

        db.session.delete(request)
        db.session.commit()

    return redirect(url_for('requests_get.get_all_user_request'))
