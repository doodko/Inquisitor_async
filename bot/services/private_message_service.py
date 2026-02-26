from typing import List

from aiogram import types

from bot.services.api_client import ApiClient
from bot.services.mixpanel_client import mp
from bot.types.enums import AnswerTypes, MixpanelEvents
from bot.types.message_answers import MessageAnswers
from bot.types.search_dto import Establishment, SearchResponse


class PrivateMessageService:
    async def process_private_message(
        self, message: types.Message
    ) -> str | List[Establishment]:
        if validation_error := await self.validate_message(message=message):
            return validation_error

        return await self.perform_search(message=message)

    @staticmethod
    async def validate_message(message: types.Message) -> str | None:
        query = message.text.lower()
        if len(query) < 3:
            answer = MessageAnswers.answer(AnswerTypes.TOO_SHORT_TEXT)
            mp.track_event(
                user=message.from_user,
                event=MixpanelEvents.TOO_SHORT_MESSAGE,
                event_properties={"message": query, "answer": answer},
            )
            return answer

        elif len(query.split()) > 3:
            answer = MessageAnswers.answer(AnswerTypes.TOO_MANY_WORDS)
            mp.track_event(
                user=message.from_user,
                event=MixpanelEvents.TOO_LONG_MESSAGE,
                event_properties={"message": query, "answer": answer},
            )
            return answer

    @staticmethod
    async def perform_search(message: types.Message) -> str | SearchResponse:
        query = message.text.lower()
        api_client = ApiClient(user=message.from_user)
        search_response = api_client.find(query=query)

        if not search_response:
            answer = MessageAnswers.answer(AnswerTypes.ERROR_MESSAGE)
            mp.track_event(
                user=message.from_user,
                event=MixpanelEvents.ERROR,
                event_properties={"message": query, "answer": answer},
            )

        elif search_response.count == 0:
            answer = MessageAnswers.answer(AnswerTypes.NO_RESULTS_FOUND)
            mp.track_event(
                user=message.from_user,
                event=MixpanelEvents.UNSUCCESSFUL_SEARCH,
                event_properties={"message": query, "answer": answer},
            )

        else:
            answer = search_response
            mp.track_event(
                user=message.from_user,
                event=MixpanelEvents.SEARCH,
                event_properties={
                    "message": query,
                    "answer": search_response.count,
                },
            )

        return answer


private_message_service = PrivateMessageService()
