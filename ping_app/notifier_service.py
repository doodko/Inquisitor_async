from datetime import datetime
from ping_app.models import Host, Zone


class NotifierService:
    def __init__(self):
        self._current_status = ("без світла", "зі світлом")
        self._new_status = ("з'явилось світло", "зникло світло")

    def get_current_state(self, instance: Zone | Host) -> str:
        return f"{instance.name} {self._current_status[instance.is_online]} вже " \
               f"{self._calculate_hours_and_minutes(instance)}"

    def get_changed_state(self, instance: Zone | Host) -> str:
        return f"{datetime.now().strftime('%H:%M')} {instance.name} {self._new_status[instance.is_online]}. " \
               f"Були {self._current_status[instance.is_online]} {self._calculate_hours_and_minutes(instance)}"

    @staticmethod
    def _calculate_hours_and_minutes(instance: Zone | Host) -> str:
        seconds_since_last_update = (datetime.now() - instance.updated_at).seconds
        hours: int = seconds_since_last_update // 3600
        minutes: int = seconds_since_last_update % 3600 // 60

        return f"{hours}:{minutes:02}"
