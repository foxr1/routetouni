import datetime
import flask
from flask import request, session
import firebase_admin
from firebase_admin import credentials, auth, exceptions
from firebase_admin import db

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://route2uni-default-rtdb.firebaseio.com/'
})


def get_all_users():
    return db.reference('users').get()


def get_mentors():
    unverified_ment = []
    verified_ment = []
    ref = db.reference('users').order_by_child('role').equal_to('Peer Mentor').get()
    print(ref)
    for key, value in ref.items():
        print(value)
        if not value['mentor_verified']:
            unverified_ment.append(value)
            print(value)
        else:
            verified_ment.append(value)
            print(value)
    return {"unverified": unverified_ment, "verified": verified_ment}


# def get_verified():
#     verified_ment = []
#     ref = db.reference('users').order_by_child('role').equal_to('Peer Mentor').get()
#     for key, value in ref.items():
#         if value['mentor_verified']:
#             verified_ment.append(value)
#
#     return verified_ment


class User:
    def __init__(self):
        self.id_token = None
        self.email = None
        self.uid = None
        self.name = None
        self.peer_mentor = None
        self.picture = None
        self.role = None
        self.school = None
        self.user_dict = None

    def clear_data(self):
        self.__init__()

    def login_user(self):
        self.id_token = request.args.get('idToken')
        # Set session expiration to 5 days.
        expires_in = datetime.timedelta(days=14)
        try:
            # Create the session cookie. This will also verify the ID token in the process.
            # The session cookie will have the same claims as the ID token.
            session_cookie = auth.create_session_cookie(self.id_token, expires_in=expires_in)

            response = flask.jsonify({'status': 'success'})
            # Set cookie policy for session cookie.
            expires = datetime.datetime.now() + expires_in

            response.set_cookie(
                'session_token', session_cookie, expires=expires, httponly=True, secure=True, samesite='Lax')
            return response
        except exceptions.FirebaseError:
            return flask.abort(401, 'Failed to create a session cookie')

    @property
    def verify_user(self):
        session_cookie = flask.request.cookies.get('session_token')
        if not session_cookie:
            return None
        else:
            try:
                decoded_claims = auth.verify_session_cookie(session_cookie, check_revoked=True)
                self.uid = decoded_claims['uid']
                if not self.uid:
                    return None
                else:
                    user_info = db.reference('users/' + self.uid).get()
                    self.name = user_info['name']
                    self.email = user_info['email']
                    self.role = user_info['role']
                    self.school = user_info['course']
                    self.picture = user_info['profilePicture']

                    self.user_dict = {"name": self.name, "email": self.email, "role": self.role, "school": self.school,
                                      "picture": self.picture, "uid": self.uid}

                    self.set_session()
                return self.user_dict

            except Exception as e:
                print("Verification Error", e)
                return None

    def set_session(self):
        session['user_dict'] = self.user_dict

    def logout_user(self):
        session_cookie = flask.request.cookies.get('session_token')
        print("logging out")
        if not session_cookie:
            self.clear_data()
            return None
        try:
            decoded_claims = auth.verify_session_cookie(session_cookie)
            auth.revoke_refresh_tokens(decoded_claims['sub'])
            response = flask.make_response(flask.redirect('/login'))
            response.set_cookie('session', expires=0)
            self.clear_data()
            print("Logout successfully")
            return response
        except auth.InvalidSessionCookieError as e:
            self.clear_data()
            print("Error Logout", e)
            return None
