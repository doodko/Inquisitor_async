import requests

from bot.enums.message_answers import AnswerTypes, MessageAnswers
from bot.services.establishment_reply_builder import EstablishmentBuilder
from bot.types.search_dto import Establishment, SearchResponse
from settings_reader import config


class ApiClient:
    def __init__(self):
        self.api_url = config.search_api

    def _request(self, endpoint, params=None):
        try:
            response = requests.get(endpoint, params=params)
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Request failed with status code: {response.status_code}")
        except Exception as e:
            print(f"Error occurred: {e}")
            return None

    def find(self, query: str) -> SearchResponse:
        endpoint = self.api_url
        params = {"search": query, "page_size": 20}

        response_data = self._request(endpoint, params)
        search_response = SearchResponse.model_validate(response_data)
        return search_response

    def _retrieve(self, slug: str) -> Establishment:
        endpoint = self.api_url + slug + "/"
        response_data = self._request(endpoint)
        establishment = Establishment.model_validate(response_data)
        return establishment

    def get_establishment_template(self, slug: str) -> str:
        establishment = self._retrieve(slug)
        if not establishment:
            return MessageAnswers.answer(AnswerTypes.ERROR_MESSAGE)

        return EstablishmentBuilder(establishment).build_establishment_card()


api_client = ApiClient()
