import requests
from aiogram.types import User

from bot.settings_reader import config
from bot.types.search_dto import Establishment, SearchResponse


class ApiClient:
    def __init__(self, user: User):
        self.api_url = config.api_url
        self.user = user

    def _request(self, endpoint: str, method: str = "GET", params=None, data=None):
        headers = {"telegram_user_id": str(self.user.id)}
        try:
            if method == "GET":
                response = requests.get(endpoint, params=params, headers=headers)
            elif method == "POST":
                response = requests.post(endpoint, json=data, headers=headers)
            else:
                raise ValueError("Unsupported HTTP method")

            if response.status_code == 200:
                return response.json()
            elif response.status_code == 403:
                self.hello_its_me()
                requests.post(
                    endpoint, json=data, headers=headers
                )  # resend post request
            else:
                print(f"Request failed with status code: {response.status_code}")
        except Exception as e:
            print(f"Error occurred: {e}")
            return None

    def find(self, query: str) -> SearchResponse:
        endpoint = self.api_url
        params = {"search": query, "page_size": 20}

        response_data = self._request(endpoint=endpoint, params=params)
        search_response = SearchResponse.model_validate(response_data)
        return search_response

    def retrieve(self, slug: str) -> Establishment:
        endpoint = self.api_url + slug + "/"
        response_data = self._request(endpoint=endpoint)
        establishment = Establishment.model_validate(response_data)
        return establishment

    def hello_its_me(self):
        endpoint = self.api_url
        data = {
            "tg_id": self.user.id,
            "first_name": self.user.first_name,
            "last_name": self.user.last_name,
            "username": self.user.username,
            "is_premium": self.user.is_premium,
        }
        response_data = self._request(endpoint=endpoint, method="POST", data=data)
        print(response_data)

    def vote(self, establishment_id: int, vote: int):
        print(f"Voting for {establishment_id}, user {self.user.id} rated it {vote}")
