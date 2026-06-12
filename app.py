import sys
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters
from config.settings import BOT_TOKEN
from bot.handlers.start import start
from bot.handlers.menu import handle_menu, handle_callback
from services.scheduler import check_reminders
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters
from bot.handlers.start import start, handle_onboarding
from services.scheduler import db
from bot.keyboards.main_menu import main_menu
from bot.handlers.menu import set_state


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data
    user_id = update.effective_user.id

    # 1. Logic for Onboarding
    if query.data == "onboarding_complete":
        await query.message.delete()
        # Send the main menu directly here
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Awesome! You are all set. What would you like to do?",
            reply_markup=main_menu() 
        )

    # 2. Logic for Delete Button
    elif query.data.startswith("del_"):
        reminder_id = query.data.split("_")[1]
        
        # Delete from Firebase
        db.collection("reminders").document(reminder_id).delete()
        current_msg_id = query.message.message_id
        chat_id = query.message.chat_id
        # Delete the message
        try:
            await query.message.delete()
            await context.bot.delete_message(chat_id=chat_id, message_id=current_msg_id - 1)
        except Exception as e:
            print(f"Error occurred while deleting message: {e}")

    elif data.startswith("edt_"):
        doc_id = data.replace("edt_", "")
        
        try:
            # Set the state so the bot remembers what to edit
            set_state(user_id, f"EDITING_TITLE_{doc_id}")
            
            # Send the prompt to the user
            await query.edit_message_text(
                text="Type the new name/title you want to assign to this reminder:"
            )
        except Exception as e:
            print(f"Error in edit button handler: {e}")
            

async def debug_sticker(update, context):
    """Temporarily catches stickers and prints their ID to the terminal"""
    file_id = update.message.sticker.file_id
    print(f"\n✅ STICKER ID COPIED: {file_id}\n")
    await update.message.reply_text("Sticker ID printed to your terminal!")

def main():
    if not BOT_TOKEN or BOT_TOKEN == "YOUR_BOT_TOKEN":
        print("❌ CRITICAL ERROR: BOT_TOKEN is missing from your environment config!")
        sys.exit(1)


    application = Application.builder().token(BOT_TOKEN).build()

    
    # Handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_menu))

    # 3. Securely schedule our continuous reminder loop sequence
    if application.job_queue:
        application.job_queue.run_repeating(check_reminders, interval=15, first=5)
        print("⏰ Native Job Queue worker attached successfully.")
    else:
        print("❌ CRITICAL ERROR: Job Queue failed to initialize! Make sure python-telegram-bot[job-queue] is installed.")
        sys.exit(1)

    # 4. Start polling for updates safely
    print("🤖 Ormayundo Bot is listening in POLLING mode...")
    application.run_polling(close_loop=False) # Prevents unexpected event loop drops on local machines

if __name__ == "__main__":
    main()