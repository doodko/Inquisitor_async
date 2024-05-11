from typing import List

from aiogram import types
from loguru import logger

from bot.enums.message_answers import AnswerTypes, MessageAnswers
from bot.services.search_service import api_client
from bot.types.search_dto import Establishment, SearchResponse


class PrivateMessageService:
    async def process_private_message(
        self, message: types.Message
    ) -> str | List[Establishment]:
        await self.log_message(message=message)
        query = message.text

        if validation_error := await self.validate_message(query=query):
            return validation_error

        return await self.perform_search(query=query)

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

    async def perform_search(self, query: str) -> str | SearchResponse:
        search_response = api_client.find(query=query)
        if not search_response:
            answer = MessageAnswers.answer(AnswerTypes.ERROR_MESSAGE)
        elif search_response.count == 0:
            answer = MessageAnswers.answer(AnswerTypes.NO_RESULTS_FOUND)
        else:
            answer = search_response

        return answer


private_message_service = PrivateMessageService()
