from flask import request, flash


class FormHelper(object):

    @staticmethod
    def check_fields_in_form(*fields):
        for f in fields:
            if isinstance(f, list):
                at_least_one_of_fields_found = False
                for sf in f:
                    if request.form.get(sf, ''):
                        at_least_one_of_fields_found = True
                        break
                if not at_least_one_of_fields_found:
                    flash("At least one of " + str(','.join(f)) + " must be filled.", "error")
                    return False
            else:
                if not request.form.get(f, ''):
                    flash("Field " + str(f) + " is missing.", "error")
                    return False

        return True
