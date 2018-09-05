from app.ref.hashes_list import HASHS_LIST
from app.helpers.text import TextHelper


class HashesHelper(object):
    HASHS_LIST = HASHS_LIST

    @staticmethod
    def validate_code(code):
        if not TextHelper.is_int(code):
            return False

        code = int(code)
        for h in HASHS_LIST:
            if int(h['code']) == code:
                return True
        return False
