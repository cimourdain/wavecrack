import os
from flask import request, flash


class FormHelper(object):

    @staticmethod
    def field_exists(field_name, form_data=True, url_args=True, form_files=True):
        if form_data and request.form.get(field_name, None):
            return True
        if url_args and request.args.get(field_name, None):
            return True
        if form_files and request.files.get(field_name, None):
            return True
        return False

    @staticmethod
    def check_fields_in_form(*fields):
        for f in fields:
            if isinstance(f, list):
                at_least_one_of_fields_found = False
                for sf in f:
                    if FormHelper.field_exists(sf):
                        at_least_one_of_fields_found = True
                        break
                if not at_least_one_of_fields_found:
                    flash("At least one of " + str(','.join(f)) + " must be filled.", "error")
                    return False
            else:
                if not FormHelper.field_exists(sf):
                    flash("Field " + str(f) + " is missing.", "error")
                    return False

        return True

    @staticmethod
    def uploaded_file_is_valid(field_name, allowed_extentions=None):
        if field_name in request.files and request.files[field_name]:
            uploaded_file = request.files[field_name]
            filename, file_extension = os.path.splitext(uploaded_file.filename)
            if not allowed_extentions or (file_extension in allowed_extentions):
                return True
        return False


