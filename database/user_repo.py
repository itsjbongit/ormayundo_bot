from config.firebase import db

COL = "users"

def get_user(user_id):
    doc = db.collection(COL).document(str(user_id)).get()
    return doc.to_dict() if doc.exists else None

def create_user(user_id, data):
    db.collection(COL).document(str(user_id)).set(data)

def update_user(user_id, data):
    db.collection(COL).document(str(user_id)).update(data)