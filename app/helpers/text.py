import re


class TextHelper(object):
    @staticmethod
    def is_int(s):
        """
        Method to check if the input arg represents an int
        :param s: <str>
        :return:<boo>
        """
        try:
            int(s)
            return True
        except ValueError:
            return False

    @staticmethod
    def check_email(email):
        pattern = r"\"?([-a-zA-Z0-9.`?{}]+@\w+\.\w+)\"?"
        return re.match(pattern, email)

    @staticmethod
    def check_mask(masks):
        """
        Method to check if a string represent a valid mask (chars after ? matches mask format)

        :param masks: <str>
        :return:
        """
        # check that all char after ? are valid
        for mask in masks.splitlines():
            start = 0
            while start < len(mask):
                mark_position = mask.find("?", start)

                if mark_position != -1:
                    print("TextHelper :: check_mask :: ? found in position " + str(mark_position) + " in string " + str(
                        mask[:start]))
                    print("TextHelper :: check_mask :: check if next char ("+mask[mark_position + 1]+") is valid")
                    if mask[mark_position + 1] not in ["l", "u", "d", "h", "H", "s", "a", "b"]:
                        print("TextHelper :: check_mask :: "+mask[mark_position + 1]+" is not valid")
                        return False
                    start = mark_position + 1
                else:
                    start = len(mask)

        return True
