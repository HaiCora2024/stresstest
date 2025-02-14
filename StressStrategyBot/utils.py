from typing import Dict, List
import time
from telegram import Message
import asyncio

def calculate_results(answers: Dict[int, int], questions: List[Dict]) -> Dict[str, float]:
    strategy_scores = {
        "избегание": [],
        "решение проблем": [],
        "позитивное переосмысление": [],
        "эмоционально-ориентированная": [],
        "поиск поддержки": []
    }

    # Группируем ответы по стратегиям
    for q in questions:
        question_id = q["id"]
        if question_id in answers:
            strategy_scores[q["strategy"]].append(answers[question_id])

    results = {}
    for strategy, scores in strategy_scores.items():
        if scores:
            max_score = len(scores) * 5  # Максимальный балл (5) умножаем на количество вопросов
            total_score = sum(scores)
            percentage = (total_score / max_score) * 100
            results[strategy] = round(percentage, 1)
        else:
            results[strategy] = 0.0

    return results

async def show_progress_animation(message: Message) -> None:
    progress_msg = await message.reply_text("Обработка результатов... 0%")
    for i in range(1, 11):
        await asyncio.sleep(0.3)
        await progress_msg.edit_text(f"Обработка результатов... {i*10}%")
    await progress_msg.delete()

def format_results_message(results: Dict[str, float], dominant_strategy: str, description: str, user_name: str = "гость") -> str:
    message = f"👋 Привет, {user_name}! Спасибо, что прошел тест!\n\n"
    message += "Меня зовут Зоя Скобельцына, я — сертифицированный коуч ICF, предприниматель, "
    message += "эксперт метода нейроинтерации и спикер TEDx. Подробнее обо мне и моих проектах "
    message += "можно узнать здесь: https://t.me/walktochange\n\n"
    message += "В своей работе я часто сталкиваюсь с запросами, которые касаются времени, "
    message += "планирования и приоритизации.\n\n"
    message += "Ты используешь разные стратегии поведения, и это здорово! Вот как они распределились:\n\n"

    # Добавляем символы для каждой стратегии
    symbols = {
        "избегание": "◆",
        "решение проблем": "★",
        "позитивное переосмысление": "⚘",
        "эмоционально-ориентированная": "♡",
        "поиск поддержки": "⚡"
    }

    # Сортируем результаты по убыванию процентов
    sorted_results = sorted(results.items(), key=lambda x: x[1], reverse=True)

    for strategy, percentage in sorted_results:
        message += f"{symbols[strategy]} {strategy.title()}: {percentage}%\n"

    message += f"\nТы чаще всего обращаешься к стратегии '{dominant_strategy}' ({results[dominant_strategy]}%). "
    message += f"Это говорит о том, что в стрессовых ситуациях ты склонен {description}.\n\n"

    message += "Помни: не существует \"правильных\" или \"неправильных\" стратегий. "
    message += "Каждая из них может быть адаптивна в определенных обстоятельствах. "
    message += "Важно осознавать разные инструменты и уметь их гибко применять в зависимости от ситуации.\n\n"

    message += "Я сделала этот файл, чтобы помочь тебе поработать с этими вопросами и определить свои приоритеты.\n\n"

    message += "Подписывайся на мой блог в Instagram и Telegram и делись этим файлом с друзьями, обнимаю:\n"
    message += "Telegram: @zoyaskobeltsyna\n"
    message += "Telegram-канал: @walktochange"

    return message