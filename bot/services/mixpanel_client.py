import mixpanel
from aiogram.types import User

from bot.settings_reader import config
from bot.types.enums import MixpanelEvents


class MixpanelClient:
    def __init__(self):
        self.mixpanel_instance = mixpanel.Mixpanel(
            config.mixpanel_token,
            consumer=mixpanel.Consumer(api_host="api-eu.mixpanel.com"),
        )

    def track_event(
        self, user_id: int, event: MixpanelEvents, event_properties: dict = None
    ):
        self.mixpanel_instance.track(str(user_id), event, event_properties)

    def update_user_properties(self, user: User):
        properties = {
            "$first_name": user.first_name,
            "$last_name": user.last_name,
            "$username": user.username,
            "is_premium": bool(user.is_premium),
        }
        self.mixpanel_instance.people_set(str(user.id), properties)


mp = MixpanelClient()
