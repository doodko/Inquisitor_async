import requests

from bot.types.search_dto import SearchResponse
from settings_reader import config


class SearchService:
    def __init__(self):
        self.api_url = config.search_api

    def _search(self, query: str):
        response = requests.get(self.api_url, params={"search": query, "page_size": 20})
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Request failed with status code: {response.status_code}")
            return None

    def find(self, query: str) -> SearchResponse | None:
        try:
            response_data = self._search(query)
            search_response = SearchResponse.model_validate(response_data)
            return search_response

        except Exception as e:
            print(f"Error occurred: {e}")
            return None


search_service = SearchService()
