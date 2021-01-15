import firebase_admin
from firebase_admin import credentials, auth
from firebase_admin import db

# Fetch the service account key JSON file contents
cred = credentials.Certificate('serviceAccountKey.json')

# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://route2uni-default-rtdb.firebaseio.com/'
})

ref = db.reference('users/3AixDYlmwbSJ0b1XpyCCoqmAhL52').get()
print(ref)
