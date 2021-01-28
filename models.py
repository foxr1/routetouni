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
    """
    :return: dictionary with all users in database
    """
    return db.reference('users').get()


def get_mentors() -> dict:
    """

    :return: dictionary
    """
    unverified_ment = []
    verified_ment = []
    ref = db.reference('users').order_by_child('role').equal_to('Peer Mentor').get()
    for key, value in ref.items():
        if not value['mentor_verified']:
            unverified_ment.append(value)
        else:
            verified_ment.append(value)
    return {"unverified": unverified_ment, "verified": verified_ment}


class User:
    """
    Class for managing users, using firebase and cookies. Implemented using this documentation  and partly adapted
    from the default google firebase management
    https://firebase.google.com/docs/auth/admin/manage-cookies

    :Authors:
        Filippos Solomonidis <F.solomonidis2@newcastle.ac.uk>
    ...
    Attributes
    ----------
    No attributes are past by default as they are filled during user authentication and the database only needs to be
    initialized once.

    Methods
    -------
    clear_data():
        clear all class attributes and the flask session, insuring complete user logout

    login_user():
        get the id token provided by frontend auth, use it to authenticate once more with the firebase db, while
        creating a cookie lasting 14 days and storing it in the users browser.

    verify_user():
        Request the saved cookie and verify against the firebase server gaining thd uid  and later querying by
        to gain all user info

    set_session():
        Set the dictionary containing important user info as a flask session object

    logout_user():
        Using the saved cookie, revoke access to it, and clear all session  and object attributes
    """

    def __init__(self):
        """
        Constructor for user information, empty by default filled when users authenticates (Note the dictionary
        containing all items is passed, the rest is added for potential functionality)
        """
        self.id_token = None
        self.email = None
        self.uid = None
        self.name = None
        self.peer_mentor = None
        self.picture = None
        self.role = None
        self.school = None
        self.verified = None
        self.user_dict = None

    def clear_data(self):
        session.clear()
        self.__init__()

    def login_user(self) -> dict:
        """
        :return: Flask wrapped response indicating if login was successfully
        """
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
        """
        :return: Dictionary containing basic user info, None if error while authenticating
        """
        session_cookie = flask.request.cookies.get('session_token')

        if not session_cookie:
            return None
        else:
            try:
                # Verify id with firebase
                decoded_claims = auth.verify_session_cookie(session_cookie, check_revoked=True)
                self.uid = decoded_claims['uid']
                if not self.uid:
                    return None
                else:
                    # Use returned id to query database for meta info
                    user_info = db.reference('users/' + self.uid).get()
                    self.name = user_info['name']
                    self.email = user_info['email']
                    self.role = user_info['role']
                    self.school = user_info['course']
                    self.picture = user_info['profilePicture']
                    self.verified = user_info['mentor_verified']
                    self.user_dict = {"name": self.name, "email": self.email, "role": self.role, "school": self.school,
                                      "picture": self.picture, "uid": self.uid, 'mentor_verified': self.verified}

                    self.set_session()
                return self.user_dict

            except Exception as e:
                print("Verification Error", e)
                return None

    def set_session(self):
        session['user_dict'] = self.user_dict

    def logout_user(self) -> object:
        """
        :return: Flask wrapped response indicating if logout was successful
        """
        session_cookie = flask.request.cookies.get('session_token')
        print("logging out")
        if not session_cookie:
            self.clear_data()
            return None
        try:
            # Verify cookie before revoking access
            decoded_claims = auth.verify_session_cookie(session_cookie)
            auth.revoke_refresh_tokens(decoded_claims['sub'])
            response = flask.jsonify({'status': 'success'})
            response.set_cookie('session', expires=0)
            self.clear_data()
            return response
        except auth.InvalidSessionCookieError as e:
            self.clear_data()
            print("Error Logout", e)
            return None
