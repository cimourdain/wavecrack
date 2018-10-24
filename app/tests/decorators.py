# third party imports
# decorator module used to maintain pytest client fixture in func
import decorator


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
            # fetch client in args
            client = args[2]

            # perform login
            from app.tests.test_login import TestLogin
            TestLogin.login(client,  admin=admin)

            return func(*args[1:], **kwargs)

        return decorator.decorator(wrapped, func)

    return decorator_func
