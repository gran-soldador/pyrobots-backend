from fastapi.testclient import TestClient
from main import app
# from db import *
# import pytest

client = TestClient(app)


# @pytest.fixture(scope="module", autouse=True)
# def reset_db():
#     db.drop_all_tables(True)
#     db.create_tables()
