import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler
from handlers import start_handler, next_question_handler, button_handler, admin_handler
import os
import sys

# Configure logging with more detailed output
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG,  # Changed to DEBUG for more detailed logs
    stream=sys.stdout  # Explicitly log to stdout
)

logger = logging.getLogger(__name__)

def main():
    # Get the bot token
    token = os.getenv('TELEGRAM_BOT_TOKEN')
    if not token:
        logger.error("No TELEGRAM_BOT_TOKEN found in environment variables!")
        return

    logger.info("Starting bot initialization...")
    logger.debug(f"Bot token found (first 5 chars): {token[:5]}")

    try:
        # Create application with error logging
        logger.info("Creating application instance...")
        application = Application.builder().token(token).build()
        logger.info("Application instance created successfully")

        # Add handlers
        logger.info("Registering command handlers...")
        application.add_handler(CommandHandler('start', start_handler))
        application.add_handler(CommandHandler('next', next_question_handler))
        application.add_handler(CommandHandler('admin', admin_handler))
        application.add_handler(CallbackQueryHandler(button_handler))
        logger.info("Handlers registered successfully")

        # Start polling with detailed error handling
        logger.info("Starting polling...")
        application.run_polling(
            allowed_updates=Update.ALL_TYPES,
            drop_pending_updates=True
        )
        logger.info("Polling started successfully")

    except Exception as e:
        logger.error(f"Critical error starting bot: {str(e)}", exc_info=True)
        raise  # Re-raise the exception for the system to handle

if __name__ == '__main__':
    try:
        logger.info("Bot script starting...")
        main()
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
        sys.exit(0)
    except Exception as e:
        logger.critical(f"Unhandled exception: {str(e)}", exc_info=True)
        sys.exit(1)