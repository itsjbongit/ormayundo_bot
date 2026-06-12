from telegram import ReplyKeyboardMarkup

def main_menu():
    keyboard = [
        ["➕ New Reminder", "📋 My Reminders"],
        ["✏️ Edit Reminder", "🗑 Delete Reminder"]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)