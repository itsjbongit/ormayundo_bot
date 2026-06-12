import os
import json
import firebase_admin
from firebase_admin import credentials, firestore
from config.settings import FIREBASE_KEY_PATH

if not firebase_admin._apps:
    # Check if the environment variable exists
    env_json = os.environ.get("FIREBASE_SERVICE_ACCOUNT")
    
    if env_json:
        # Use the string from Render's environment
        cred_dict = json.loads(env_json)
        cred = credentials.Certificate(cred_dict)
    else:
        # Fallback to your local JSON file (for local development)
        cred = credentials.Certificate(FIREBASE_KEY_PATH)
        
    firebase_admin.initialize_app(cred)

db = firestore.client()