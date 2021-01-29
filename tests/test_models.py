import models
from firebase_admin import db


# Test that all users in the database can be retrieved
# Expected outcome = True
def test_get_all_users():
    assert models.get_all_users() == db.reference('users').get()


def test_get_mentors():
    unverified_ment = []
    verified_ment = []
    ref = db.reference('users').order_by_child('role').equal_to('Peer Mentor').get()
    for key, value in ref.items():
        if not value['mentor_verified']:
            unverified_ment.append(value)
        else:
            verified_ment.append(value)
    assert models.get_mentors() == {"unverified": unverified_ment, "verified": verified_ment}
