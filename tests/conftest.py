from fastapi.testclient import TestClient
from main import app
from db import db
from endpoints.functions_jwt import authenticated_user
import pytest

_client = TestClient(app)


@pytest.fixture()
def client():
    return _client


@pytest.fixture()
def mocked_login():
    app.dependency_overrides = {authenticated_user: lambda: 1}
    yield
    app.dependency_overrides = {}
    return


@pytest.fixture()
def loggedin_client(client, mocked_login):
    return client


@pytest.fixture(autouse=True)
def reset_db():
    db.drop_all_tables(True)
    db.create_tables()
