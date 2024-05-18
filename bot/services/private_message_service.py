from typing import List

from aiogram import types
from loguru import logger

from bot.services.api_client import ApiClient
from bot.types.enums import AnswerTypes
from bot.types.message_answers import MessageAnswers
from bot.types.search_dto import Establishment, SearchResponse


class PrivateMessageService:
    async def process_private_message(
        self, message: types.Message
    ) -> str | List[Establishment]:
        await self.log_message(message=message)

        if validation_error := await self.validate_message(query=message.text):
            return validation_error

        return await self.perform_search(message=message)

    @staticmethod
    async def log_message(message: types.Message):
        log_text = f"other messages | {message.from_user.full_name} | {message.text}"
        logger.bind(private=True).info(log_text)

    @staticmethod
    async def validate_message(query: str) -> str | None:
        if len(query) < 3:
            return MessageAnswers.answer(AnswerTypes.TOO_SHORT_TEXT)
        elif len(query.split()) > 3:
            return MessageAnswers.answer(AnswerTypes.TOO_MANY_WORDS)

    @staticmethod
    async def perform_search(message: types.Message) -> str | SearchResponse:
        query = message.text
        api_client = ApiClient(user=message.from_user)
        search_response = api_client.find(query=query)
        if not search_response:
            answer = MessageAnswers.answer(AnswerTypes.ERROR_MESSAGE)
        elif search_response.count == 0:
            answer = MessageAnswers.answer(AnswerTypes.NO_RESULTS_FOUND)
        else:
            answer = search_response

        return answer


private_message_service = PrivateMessageService()
