import pytest

from app import create_app, db, register_routes



@pytest.fixture
def client():
    # build app
    app = create_app('testing')
    register_routes(app)

    # enter context
    app_ctx = app.app_context()
    app_ctx.push()

    # reset and init database
    from app.models.user import User
    from app.models.cracks.entity import Crack
    from app.models.cracks.request import CrackRequest

    db.reflect()
    db.drop_all()

    db.create_all()
    User.insert_default_users()

    # setup client
    client = app.test_client(use_cookies=True)

    yield client

    db.session.remove()
    app_ctx.pop()
