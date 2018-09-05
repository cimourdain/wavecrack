from app.ref.hashes_list import HASHS_LIST


class HashesHelper(object):
    HASHS_LIST = HASHS_LIST

    @staticmethod
    def validate_code(code):
        for h in HASHS_LIST:
            if int(h['code']) == int(code):
                return True
        return False
