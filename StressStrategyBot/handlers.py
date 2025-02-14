from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from database import Database
from utils import calculate_results, show_progress_animation, format_results_message
import random
import logging

# Configure logging
logger = logging.getLogger(__name__)

db = Database()

# Подбадривающие сообщения между вопросами
ENCOURAGEMENT_MESSAGES = [
    "Отлично! Продолжаем...",
    "Хороший ответ! Идём дальше...",
    "Ты молодец! Следующий вопрос...",
    "Интересный выбор! Двигаемся дальше...",
    "Уже почти половина пройдена! Продолжай в том же духе...",
    "Замечательно справляешься! Продолжим...",
    "Осталось совсем немного! Ты прекрасно справляешься...",
    "Каждый ответ приближает нас к пониманию твоих стратегий...",
    "Отлично продвигаемся! Следующий вопрос..."
]

async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        user_id = update.effective_user.id
        user_name = update.effective_user.first_name or "гость"
        logger.info(f"Start command received from user {user_id}")

        db.start_user_session(user_id)

        welcome_text = (
            f"👋 Привет, {user_name}!\n\n"
            "Этот тест поможет тебе определить твои основные стратегии поведения в стрессовых ситуациях.\n"
            "Тебе предстоит ответить на несколько вопросов, оценивая каждое утверждение по шкале от 1 до 5:\n\n"
            "1 - Почти никогда\n"
            "2 - Редко\n"
            "3 - Иногда\n"
            "4 - Часто\n"
            "5 - Почти всегда\n\n"
            "Готов начать? Нажми /next для первого вопроса!"
        )

        await update.message.reply_text(welcome_text)
        logger.info(f"Welcome message sent to user {user_id}")
    except Exception as e:
        logger.error(f"Error in start_handler: {str(e)}", exc_info=True)
        await update.message.reply_text("Произошла ошибка. Пожалуйста, попробуйте позже или свяжитесь с администратором.")

async def send_question(message, current_q: int, questions: list) -> None:
    try:
        keyboard = [
            [InlineKeyboardButton(str(i), callback_data=f"answer_{i}") for i in range(1, 6)]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        question_text = f"Вопрос {current_q + 1}/{len(questions)}:\n{questions[current_q]['question']}"

        # Добавляем прогресс-бар
        total = len(questions)
        progress = int((current_q + 1) / total * 10)
        progress_bar = "▓" * progress + "░" * (10 - progress)
        question_text += f"\n\nПрогресс: [{progress_bar}] {int((current_q + 1) / total * 100)}%"

        await message.reply_text(question_text, reply_markup=reply_markup)
        logger.info(f"Question {current_q + 1} sent successfully")
    except Exception as e:
        logger.error(f"Error in send_question: {str(e)}", exc_info=True)
        await message.reply_text("Произошла ошибка при отправке вопроса. Пожалуйста, попробуйте /next еще раз.")

async def next_question_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        user_id = update.effective_user.id
        user_name = update.effective_user.first_name or "гость"
        session = db.get_user_session(user_id)
        logger.info(f"Next command received from user {user_id}")

        if not session:
            await update.message.reply_text(f"{user_name}, пожалуйста, начни тест с команды /start")
            return

        questions = db.get_questions()
        current_q = session["current_question"]

        if current_q >= len(questions):
            await show_progress_animation(update.message)
            results = calculate_results(session["answers"], questions)
            dominant_strategy = max(results.items(), key=lambda x: x[1])[0]
            description = db.get_strategy_description(dominant_strategy)

            result_message = format_results_message(results, dominant_strategy, description, user_name)
            keyboard = [[InlineKeyboardButton("Получить файл-рефлексию", callback_data="download_file")]]
            reply_markup = InlineKeyboardMarkup(keyboard)

            await update.message.reply_text(result_message, reply_markup=reply_markup)
            db.mark_test_completed(user_id)
            logger.info(f"Test completed for user {user_id}")
            return

        await send_question(update.message, current_q, questions)
    except Exception as e:
        logger.error(f"Error in next_question_handler: {str(e)}", exc_info=True)
        await update.message.reply_text("Произошла ошибка. Пожалуйста, попробуйте позже или свяжитесь с администратором.")

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        query = update.callback_query
        await query.answer()

        user_id = update.effective_user.id
        user_name = update.effective_user.first_name or "гость"
        session = db.get_user_session(user_id)
        logger.info(f"Button pressed by user {user_id}: {query.data}")

        if not session:
            await query.message.reply_text(f"{user_name}, пожалуйста, начни тест с команды /start")
            return

        questions = db.get_questions()
        current_q = session["current_question"]

        if query.data.startswith("answer_"):
            answer = int(query.data.split("_")[1])
            db.save_answer(user_id, current_q, answer)
            session["current_question"] += 1

            # Показываем подбадривающее сообщение каждые 3 ответа
            if session["current_question"] < len(questions):
                if (current_q + 1) % 3 == 0:  # каждый третий ответ
                    encouragement = random.choice(ENCOURAGEMENT_MESSAGES)
                    await query.message.reply_text(encouragement)
                await send_question(query.message, session["current_question"], questions)
            else:
                await show_progress_animation(query.message)
                results = calculate_results(session["answers"], questions)
                dominant_strategy = max(results.items(), key=lambda x: x[1])[0]
                description = db.get_strategy_description(dominant_strategy)

                result_message = format_results_message(results, dominant_strategy, description, user_name)
                keyboard = [[InlineKeyboardButton("Получить файл-рефлексию", callback_data="download_file")]]
                reply_markup = InlineKeyboardMarkup(keyboard)

                await query.message.reply_text(result_message, reply_markup=reply_markup)
                db.mark_test_completed(user_id)
                logger.info(f"Test completed for user {user_id}")

        elif query.data == "download_file":
            await query.message.reply_text(
                "Спасибо за интерес к материалам! Следи за обновлениями в моих социальных сетях:\n\n"
                "Telegram: @zoyaskobeltsyna\n"
                "Telegram-канал: @walktochange"
            )
            logger.info(f"Download file requested by user {user_id}")
    except Exception as e:
        logger.error(f"Error in button_handler: {str(e)}", exc_info=True)
        await query.message.reply_text("Произошла ошибка. Пожалуйста, попробуйте позже или свяжитесь с администратором.")

async def admin_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        user_id = update.effective_user.id
        user_name = update.effective_user.first_name or "гость"
        logger.info(f"Admin command received from user {user_id}")

        if not db.is_admin(user_id):
            await update.message.reply_text(f"{user_name}, у тебя нет доступа к этой команде.")
            return

        stats = db.get_statistics()
        stats_message = (
            f"📊 {user_name}, вот статистика использования бота:\n\n"
            f"Всего пользователей: {stats['total_users']}\n"
            f"Завершенных тестов: {stats['completed_tests']}"
        )
        await update.message.reply_text(stats_message)
        logger.info(f"Admin stats sent to user {user_id}")
    except Exception as e:
        logger.error(f"Error in admin_handler: {str(e)}", exc_info=True)
        await update.message.reply_text("Произошла ошибка при получении статистики.")