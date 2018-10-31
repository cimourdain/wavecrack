# third party imports
# decorator module used to maintain pytest client fixture in func
import decorator
from flask.testing import FlaskClient


def login_required(admin=False, *dec_args, **dec_kwargs):
    """
    decorator used to login before performing a test.

    usage:
    @login_required(admin=True)
    def test_...():
        ...

    :param admin : <bool> login as admin?
    """
    def decorator_func(func):

        def wrapped(*args, **kwargs):
            assert len(args) > 2, \
                "login_required (decorator) :: client param seems to be missing in arguments for function "+str(func)
            # fetch client in args
            client = args[2]
            assert type(client) == FlaskClient, \
                "login_required (decorator) :: client is not a instance of FlaskClient but "+str(type(client)) + \
                " for function "+str(func)

            # perform login
            from app.tests.test_login import TestLogin
            TestLogin.login(client,  admin=admin)

            return func(*args[1:], **kwargs)

        return decorator.decorator(wrapped, func)

    return decorator_func
