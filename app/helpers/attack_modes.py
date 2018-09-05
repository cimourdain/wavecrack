from app.ref.attack_modes import ATTACK_MODES
from app.helpers.text import TextHelper


class AttackModeHelper(object):
    ATTACK_MODES = ATTACK_MODES

    @staticmethod
    def validate_code(code):
        if not TextHelper.is_int(code):
            return False

        code = int(code)
        for a in ATTACK_MODES:
            if int(a['code']) == code:
                return True
        return False
