from database.user_repo import get_user, create_user, update_user
from config.settings import DEFAULT_TIMEZONE
from datetime import datetime, timezone

def ensure_user(user):
    user_id = str(user.id)
    existing = get_user(user_id)
    if existing:
        return existing

    new_user = {
        "telegram_id": user.id,
        "first_name": user.first_name,
        "username": user.username,
        "state": "IDLE",
        "timezone": DEFAULT_TIMEZONE,
        "temp": {},
        "created_at": datetime.now(timezone.utc).isoformat()
    }
    create_user(user_id, new_user)
    return new_user

def set_state(user_id, state):
    update_user(user_id, {"state": state})

def set_temp(user_id, key, value):
    user = get_user(user_id)
    temp = user.get("temp", {}) if user else {}
    temp[key] = value
    update_user(user_id, {"temp": temp})

def clear_temp(user_id):
    update_user(user_id, {"temp": {}})