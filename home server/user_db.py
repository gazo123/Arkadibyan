import json
import os
import secrets

USER_DB = "user_db.json"

def load_users():
    if os.path.exists(USER_DB):
        with open(USER_DB, "r") as f:
            return json.load(f)
    return {}

def save_users(data):
    with open(USER_DB, "w") as f:
        json.dump(data, f, indent=4)

def register_user(uid):
    db = load_users()
    if uid not in db:
        db[uid] = secrets.token_hex(16)
        save_users(db)
    return db[uid]
