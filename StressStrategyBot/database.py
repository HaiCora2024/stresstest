import json
from typing import Dict, List, Optional
import os
import logging

# Configure logging
logger = logging.getLogger(__name__)

class Database:
    def __init__(self):
        self.users = {}
        self.admins = {"123456789"}  # Add admin Telegram IDs here
        self.user_sessions = {}
        logger.info("Database initialized")

    def start_user_session(self, user_id: int) -> None:
        try:
            self.user_sessions[user_id] = {
                "current_question": 0,
                "answers": {},
                "completed": False
            }
            logger.info(f"Started new session for user {user_id}")
        except Exception as e:
            logger.error(f"Error starting session for user {user_id}: {str(e)}", exc_info=True)

    def get_user_session(self, user_id: int) -> Optional[Dict]:
        try:
            session = self.user_sessions.get(user_id)
            logger.debug(f"Retrieved session for user {user_id}: {'Found' if session else 'Not found'}")
            return session
        except Exception as e:
            logger.error(f"Error getting session for user {user_id}: {str(e)}", exc_info=True)
            return None

    def save_answer(self, user_id: int, question_id: int, answer: int) -> None:
        try:
            if user_id in self.user_sessions:
                self.user_sessions[user_id]["answers"][question_id] = answer
                logger.info(f"Saved answer for user {user_id}, question {question_id}: {answer}")
            else:
                logger.warning(f"Attempted to save answer for non-existent session: user {user_id}")
        except Exception as e:
            logger.error(f"Error saving answer for user {user_id}: {str(e)}", exc_info=True)

    def is_admin(self, user_id: int) -> bool:
        is_admin = str(user_id) in self.admins
        logger.debug(f"Admin check for user {user_id}: {is_admin}")
        return is_admin

    def get_statistics(self) -> Dict:
        try:
            stats = {
                "total_users": len(self.user_sessions),
                "completed_tests": len([u for u in self.user_sessions.values() if u["completed"]])
            }
            logger.info(f"Retrieved statistics: {stats}")
            return stats
        except Exception as e:
            logger.error(f"Error getting statistics: {str(e)}", exc_info=True)
            return {"total_users": 0, "completed_tests": 0}

    def mark_test_completed(self, user_id: int) -> None:
        try:
            if user_id in self.user_sessions:
                self.user_sessions[user_id]["completed"] = True
                logger.info(f"Marked test as completed for user {user_id}")
            else:
                logger.warning(f"Attempted to mark completion for non-existent session: user {user_id}")
        except Exception as e:
            logger.error(f"Error marking test completion for user {user_id}: {str(e)}", exc_info=True)

    def get_questions(self) -> List[Dict]:
        try:
            questions_file = 'questions.json'
            logger.debug(f"Attempting to read questions from {questions_file}")

            if not os.path.exists(questions_file):
                logger.error(f"Questions file not found: {questions_file}")
                return []

            with open(questions_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                questions = data["questions"]
                logger.info(f"Successfully loaded {len(questions)} questions")
                return questions
        except json.JSONDecodeError as e:
            logger.error(f"JSON parsing error in questions file: {str(e)}", exc_info=True)
            return []
        except Exception as e:
            logger.error(f"Error loading questions: {str(e)}", exc_info=True)
            return []

    def get_strategy_description(self, strategy: str) -> str:
        try:
            questions_file = 'questions.json'
            logger.debug(f"Attempting to read strategy descriptions from {questions_file}")

            if not os.path.exists(questions_file):
                logger.error(f"Questions file not found: {questions_file}")
                return ""

            with open(questions_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                description = data["strategy_descriptions"].get(strategy, "")
                logger.debug(f"Retrieved description for strategy '{strategy}': {'Found' if description else 'Not found'}")
                return description
        except json.JSONDecodeError as e:
            logger.error(f"JSON parsing error in questions file: {str(e)}", exc_info=True)
            return ""
        except Exception as e:
            logger.error(f"Error getting strategy description: {str(e)}", exc_info=True)
            return ""