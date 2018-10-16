from app.ref.attack_modes import ATTACK_MODES
from app.helpers.text import TextHelper


class AttackModeHelper(object):
    ATTACK_MODES = ATTACK_MODES

    @staticmethod
    def validate_code(code):
        """
        Method used to validate that an attack mode is valid (mathes an allowed attack mode code in ATTACK_MODES ref)

        :param code:<int> or <str>
        :return:
        """
        if not TextHelper.is_int(code):
            return False

        code = int(code)
        for a in ATTACK_MODES:
            if int(a['code']) == code:
                return True
        return False
