from datetime import datetime
from ping_app.models import Host, Zone


class NotifierService:
    def __init__(self):
        self._emodji = ('🤬', '🤩')
        self._current_status = ("без електроенергії", "з електроенергією")
        self._new_status = ("з'явилось світло", "зникло світло")

    def get_current_state(self, instance: Zone | Host) -> str:
        status = instance.is_online
        return f"{self._emodji[status]} <b>{instance.name}</b> {self._new_status[not status]} " \
               f"<b>{instance.updated_at.strftime('%d/%m/%Y')}</b> о <b>{instance.updated_at.strftime('%H:%M')}</b>, " \
               f"{self._current_status[status]} вже {self._calculate_hours_and_minutes(instance)}"

    def get_changed_state(self, instance: Zone | Host) -> str:
        return f"{self._emodji[not instance.is_online]} <b>{instance.name}</b> {self._new_status[instance.is_online]}. " \
               f"Були {self._current_status[instance.is_online]} {self._calculate_hours_and_minutes(instance)}"

    @staticmethod
    def _calculate_hours_and_minutes(instance: Zone | Host) -> str:
        time_since_last_update = datetime.now() - instance.updated_at
        seconds_since_last_update = time_since_last_update.seconds
        days: int = time_since_last_update.days
        days_str = str(days) + ' дн. ' if days else ''
        hours: int = seconds_since_last_update // 3600
        hours_str = str(hours) + ' год. ' if hours else ''
        minutes: int = seconds_since_last_update % 3600 // 60

        return f"{days_str}{hours_str}{minutes:02} хв."
