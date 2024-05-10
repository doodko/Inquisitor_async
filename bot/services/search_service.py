import requests

from bot.types.search_dto import SearchResponse
from settings_reader import config


class SearchService:
    def __init__(self):
        self.api = config.search_api

    def find(self, query: str) -> SearchResponse | None:
        url = f"{self.api}?search={query}&page_size=20"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                response_data = response.json()
                search_response = SearchResponse.model_validate(response_data)
                return search_response
            else:
                print(f"Request failed with status code: {response.status_code}")
                return None
        except Exception as e:
            print(f"Error occurred: {e}")
            return None


search_service = SearchService()
