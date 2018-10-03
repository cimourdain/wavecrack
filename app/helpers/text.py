
class TextHelper(object):
    @staticmethod
    def is_int(s):
        try:
            int(s)
            return True
        except ValueError:
            return False

    @staticmethod
    def check_mask(masks):
        # check that all char after ? are valid
        for mask in masks.splitlines():
            start = 0
            while start < len(mask):
                mark_position = mask.find("?", start)
                if mark_position != -1:
                    if mask[mark_position + 1] not in ["l", "u", "d", "h", "H", "s", "a", "b"]:
                        return False
                    start = mark_position + 1
                else:
                    start = len(mask)

        return True
