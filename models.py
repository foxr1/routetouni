import datetime
import flask
from flask import request
import firebase_admin
from firebase_admin import credentials, auth, exceptions


class User:

    def __init__(self):
        cred = credentials.Certificate("serviceAccountKey.json")
        firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://route2uni-default-rtdb.firebaseio.com/'
        })
        self.id_token = ""
        self.email = None
        self.uid = None

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
                'session', session_cookie, expires=expires, httponly=True, secure=True)
            return response
        except exceptions.FirebaseError:
            return flask.abort(401, 'Failed to create a session cookie')

    def verify_user(self):
        session_cookie = flask.request.cookies.get('session')
        if not session_cookie:
            print("No Cookie")
        else:
            try:
                decoded_claims = auth.verify_session_cookie(session_cookie, check_revoked=True)
                print(decoded_claims)
                self.uid = decoded_claims['uid']
                self.email = decoded_claims['email']
                return self.uid

            except auth.InvalidSessionCookieError as e:
                print(e)
                print("Verification Error")

    def logout_user(self):
        session_cookie = flask.request.cookies.get('session')
        try:
            decoded_claims = auth.verify_session_cookie(session_cookie)
            auth.revoke_refresh_tokens(decoded_claims['sub'])
            response = flask.make_response(flask.redirect('/login'))
            response.set_cookie('session', expires=0)
            self.id_token = ""
            self.email = None
            self.uid = None
            return response
        except auth.InvalidSessionCookieError:
            print("Error Logout")