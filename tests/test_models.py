import models
from firebase_admin import db


# Test that all users in the database can be retrieved
# Expected outcome = True
def test_get_all_users():
    assert models.get_all_users() == db.reference('users').get()


