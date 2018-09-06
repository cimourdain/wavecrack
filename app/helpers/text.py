
class TextHelper(object):
    @staticmethod
    def is_int(s):
        try:
            int(s)
            return True
        except ValueError:
            return False

    @staticmethod
    def check_mask(mask):
        for c in mask:
            if c not in ['?', 'l', 'u', 'd', 's', 'a', 'b', '']:
                return False
        return True
