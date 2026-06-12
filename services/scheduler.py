from config.firebase import db
from datetime import datetime, timezone
from google.cloud.firestore import FieldFilter
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

async def check_reminders(context):
    """
    Automated cyclic runtime operation.
    Natively bound within the PTB Async Thread ecosystem via Context Loop allocations.
    """
    now = datetime.now(timezone.utc)
    
    # Query database for targets scheduled past runtime current bounds
    # Query database for targets scheduled past runtime current bounds
    reminders = db.collection("reminders") \
        .where(filter=FieldFilter("status", "==", "ACTIVE")) \
        .where(filter=FieldFilter("trigger_time", "<=", now)) \
        .stream()
        
    for r in reminders:
        data = r.to_dict()
        reminder_id = r.id
        
        try:

            db.collection("reminders").document(reminder_id).update({
                "status": "SENT"
            })
            my_sticker_id = "CAACAgIAAxkBAAOKaiuaVBtIwhvKBf7SlP-H03qQvyEAAjRcAALU5DlKLIChqO5VZDQ8BA"
           

            await context.bot.send_sticker(
                chat_id=data["user_id"],
                sticker=my_sticker_id
            )

            keyboard = [[InlineKeyboardButton("🗑 Dismiss/Delete", callback_data=f"del_{reminder_id}")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            # 3. Send the text details
            title = data.get('title', 'Reminder')
            
            message = (
            "🔔 <b>ORMAYUNDO ALERT</b>\n"
            "━━━━━━━━━━━━━━━━━━\n"
            f"📌 <b>Task:</b> {data.get('title', 'Untitled')}\n"
            f"⏰ <b>Original Time:</b> {data.get('time_text', 'N/A')}\n"
            "━━━━━━━━━━━━━━━━━━\n"
            "<i>Don't forget to complete this action!</i>"
        )

        # Send the bulky notification
            await context.bot.send_message(
                chat_id=data["user_id"],
                text=message,
                parse_mode="HTML",
                reply_markup=reply_markup
            )
            # Flag processing mutations
            db.collection("reminders").document(reminder_id).update({
                "status": "SENT"
            })
        except Exception as e:
            print(f"Failed to cleanly dispatch notification transaction execution id {reminder_id}: {e}")

# In services/scheduler.py

async def check_for_missed_reminders(context):
    now = datetime.now(timezone.utc)
    # Find anything that was supposed to go off, is ACTIVE, but the time has passed
    missed_reminders = db.collection("reminders") \
        .where(filter=FieldFilter("status", "==", "ACTIVE")) \
        .where(filter=FieldFilter("trigger_time", "<", now)) \
        .stream()

    for r in missed_reminders:
        # Trigger these immediately since the bot was offline when they were due
        await send_reminder(r.id, r.to_dict(), context.bot)