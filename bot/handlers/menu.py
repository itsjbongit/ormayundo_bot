from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from database.user_repo import get_user
from services.user_service import set_state, set_temp, clear_temp
from config.firebase import db
import dateparser
from datetime import datetime, timezone
import pytz
from google.cloud.firestore import FieldFilter

async def handle_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user_id = str(update.effective_user.id)
    user = get_user(user_id) or {}
    state = user.get("state", "IDLE")
    user_tz = user.get("timezone", "Asia/Kolkata")

    # --- FLOW 1: NEW REMINDER ---
    if text == "➕ New Reminder":
        set_state(user_id, "WAITING_TITLE")
        await update.message.reply_text("What should I remind you about?")
        return

    if state == "WAITING_TITLE":
        set_temp(user_id, "title", text)
        set_state(user_id, "WAITING_TIME")
        await update.message.reply_text("When should I remind you?\n(Ex: 'in 25 mins', 'tomorrow 3pm', 'at 18:00')")
        return

    if state == "WAITING_TIME":
        title = user.get("temp", {}).get("title", "Reminder")
        
        # 1. Parse the text into a datetime object
        settings = {'TIMEZONE': user_tz, 'TO_TIMEZONE': 'UTC', 'RETURN_AS_TIMEZONE_AWARE': True}
        parsed_time = dateparser.parse(text, settings=settings)

        # 2. Check if the parser failed (returns None)
        if not parsed_time:
            await update.message.reply_text("❌ I couldn't understand that time format. Try again (e.g., 'in 1 hour'):")
            return

        # 3. Snap to the exact start of the minute (Delay fix)
        parsed_time = parsed_time.replace(second=0, microsecond=0)

        # 4. Check if the time is in the past
        if parsed_time < datetime.now(timezone.utc):
            await update.message.reply_text("❌ That time is in the past! Please provide a future time:")
            return

        # 5. Save to Database
        db.collection("reminders").add({
            "user_id": int(user_id),
            "title": title,
            "time_text": text,
            "trigger_time": parsed_time, 
            "status": "ACTIVE"
        })

        clear_temp(user_id)
        set_state(user_id, "IDLE")

        # 6. Format and send confirmation
        local_time = parsed_time.astimezone(pytz.timezone(user_tz)).strftime('%Y-%m-%d %I:%M %p')
        await update.message.reply_text(
            f"✅ **Reminder Scheduled!**\n\n📌 **TASK:** {title}\n\n⏰ **DUE ON:** {local_time} ({user_tz})",
            reply_markup=from_main_menu_import(),
            parse_mode="Markdown"
        )
        return

    # --- FLOW 2: LIST REMINDERS ---
    if text == "📋 My Reminders":
        reminders = db.collection("reminders") \
        .where(filter=FieldFilter("user_id", "==", int(user_id))) \
        .where(filter=FieldFilter("status", "==", "ACTIVE")) \
        .stream()
        msg = "📋 **Your Scheduled Reminders:**\n\n"
        count = 0
        for r in reminders:
            count += 1
            data = r.to_dict()
            loc_t = data["trigger_time"].astimezone(pytz.timezone(user_tz)).strftime('%I:%M %p')
            msg += f"• **{data['title']}** — ⏰ {loc_t}\n"
        
        if count == 0:
            msg = "You have no active reminders right now! 🎉"
        await update.message.reply_text(msg, parse_mode="Markdown")
        return

    # --- FLOW 3: DELETE REMINDERS (INLINE INTERACTIVE) ---
    if text == "🗑 Delete Reminder":
        reminders = db.collection("reminders") \
        .where(filter=FieldFilter("user_id", "==", int(user_id))) \
        .where(filter=FieldFilter("status", "==", "ACTIVE")) \
        .stream()
        buttons = []
        for r in reminders:
            data = r.to_dict()
            buttons.append([InlineKeyboardButton(f"❌ {data['title']}", callback_data=f"del_{r.id}")])
        
        if not buttons:
            await update.message.reply_text("Nothing to delete.")
            return
            
        await update.message.reply_text("Select a reminder to clear:", reply_markup=InlineKeyboardMarkup(buttons))
        return

    # --- FLOW 4: EDIT REMINDERS ---
    if text == "✏️ Edit Reminder":
        reminders = db.collection("reminders") \
        .where(filter=FieldFilter("user_id", "==", int(user_id))) \
        .where(filter=FieldFilter("status", "==", "ACTIVE")) \
        .stream()
        buttons = []
        for r in reminders:
            data = r.to_dict()
            buttons.append([InlineKeyboardButton(f"📝 {data['title']}", callback_data=f"edt_{r.id}")])
        
        if not buttons:
            await update.message.reply_text("No active reminders to edit.")
            return
            
        await update.message.reply_text("Select a reminder to change its text:", reply_markup=InlineKeyboardMarkup(buttons))
        return

    # Handle update steps for title modifications
    if state.startswith("EDITING_TITLE_"):
        rem_id = state.replace("EDITING_TITLE_", "")
        db.collection("reminders").document(rem_id).update({"title": text})
        set_state(user_id, "IDLE")
        await update.message.reply_text(f"✅ Title successfully updated to: **{text}**", parse_mode="Markdown", reply_markup=from_main_menu_import())
        return

    await update.message.reply_text("Choose an option from the menu panels below:", reply_markup=from_main_menu_import())

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Processes Inline Execution Signals"""
    query = update.callback_query
    await query.answer()
    user_id = str(update.effective_user.id)
    data = query.data

    if data.startswith("del_"):
        doc_id = data.replace("del_", "")
        db.collection("reminders").document(doc_id).update({"status": "DELETED"})
        await query.edit_message_text("🗑 Reminder successfully removed permanently.")
        
    elif data.startswith("edt_"):
        doc_id = data.replace("edt_", "")
        set_state(user_id, f"EDITING_TITLE_{doc_id}")
        await query.edit_message_text("Type the new name/title you want to assign to this reminder:")

def from_main_menu_import():
    from bot.keyboards.main_menu import main_menu
    return main_menu()