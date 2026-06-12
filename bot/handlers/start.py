from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from services.user_service import ensure_user
from bot.keyboards.main_menu import main_menu

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    ensure_user(user)

    welcome_text = (
        "👋 **Welcome to Ormayundo!**\n\n"
        "Because this is a reminder bot, it is completely useless if your notifications are muted. Let's fix that first.\n\n"
        "🚨 **IMPORTANT SETUP:**\n"
        "1. Go to this bot's profile (tap the bot's name at the top).\n"
        "2. Ensure **Notifications** are turned **ON**.\n\n"
        "Once you have done that, click the button below to unlock the bot!"
    )

    # Create an inline button for confirmation
    keyboard = [
        [InlineKeyboardButton("✅ I have unmuted the bot!", callback_data="onboarding_complete")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        welcome_text,
        reply_markup=reply_markup,
        parse_mode="Markdown"
    )


async def handle_onboarding(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Listens for the inline button click and unlocks the bot."""
    query = update.callback_query
    
    # Required by Telegram to stop the loading animation on the button
    await query.answer() 

    if query.data == "onboarding_complete":
        # Delete the onboarding message
        await query.message.delete()

        # Send the actual main menu
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Awesome! You are all set. What would you like to do?",
            reply_markup=main_menu()
        )