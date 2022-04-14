import firebase_admin
from firebase_admin import db

cred_obj = firebase_admin.credentials.Certificate('key.json')
default_app = firebase_admin.initialize_app(cred_obj,
                                            {'databaseURL': 'https://educationbot-8893a-default-rtdb.firebaseio.com/'})

ref_user = db.reference("/users")
ref_course = db.reference("/courses")


