from datetime import datetime, timedelta
from random import sample

from sqlalchemy import select

from ping_app.db import Session
from ping_app.models import Period, ElectricityAvailability


class StatisticsService:
    def __init__(self, session: Session = Session()):
        self.session = session

    def make_daily_stats_message(self, date: datetime) -> str:
        stats = self._get_daily_stats(date=date)
        emoji = self._get_emoji()
        light_on = self._get_light_on_phrase()

        message = f"Спостереження за <b>{stats.date}</b>:\n\n" \
                  f"{emoji[0]} Перші лінії {light_on[0]} <b>{self._get_daily_duration(stats.zone1_duration)}</b>\n" \
                  f"{emoji[1]} ЛУ, Соборна {light_on[1]} <b>{self._get_daily_duration(stats.zone2_duration)}</b>"

        return message

    def make_weekly_stats_message(self) -> str:
        stats = self._get_weekly_stats()
        zone1_duration = [day.zone1_duration for day in stats]
        zone2_duration = [day.zone2_duration for day in stats]
        emoji = self._get_emoji()
        light_on = self._get_light_on_phrase()

        message = "Cпостереження за <b>останній тиждень</b>:\n\n"
        message += f"{emoji[0]} <b>Перші лінії</b> {light_on[0]} {self._get_analytics(zone1_duration)}\n\n"
        message += f"{emoji[1]} <b>ЛУ, Соборна</b> {light_on[1]} {self._get_analytics(zone2_duration)}\n\n"
        message += f"Цікавить конкретна дата? Введіть команду в форматі:" \
                   f"\n<code>/stats {(datetime.today() - timedelta(days=1)).date()}</code>"

        return message

    def _create_daily_stats(self, date: datetime) -> ElectricityAvailability:
        zone1_duration, zone2_duration = self._calculate_daily_stats(date=date)
        new_stats = ElectricityAvailability(date=date, zone1_duration=zone1_duration, zone2_duration=zone2_duration)

        self.session.add(new_stats)
        self.session.commit()

        return new_stats

    def _get_daily_stats(self, date: datetime) -> ElectricityAvailability:
        stats = self.session.scalar(select(ElectricityAvailability).where(ElectricityAvailability.date == date.date()))
        if not stats:
            stats = self._create_daily_stats(date=date)
        return stats

    def _get_weekly_stats(self) -> list[ElectricityAvailability]:
        stats = self.session.query(ElectricityAvailability).order_by(ElectricityAvailability.date.desc()).limit(7).all()

        yesterday = datetime.today() - timedelta(days=1)
        if stats[0].date < yesterday.date():
            self._create_daily_stats(yesterday)

        return stats

    def _calculate_daily_stats(self, date: datetime) -> tuple[timedelta, timedelta]:
        zone1_duration = timedelta(0)
        zone2_duration = timedelta(0)

        daily_periods = self._get_periods_by_date(search_date=date)
        for period in daily_periods:
            if period.zone == 1:
                zone1_duration += self._count_period_duration(period=period, search_date=date)
            elif period.zone == 2:
                zone2_duration += self._count_period_duration(period=period, search_date=date)

        return zone1_duration, zone2_duration

    def _get_periods_by_date(self, search_date: datetime):
        periods = self.session.query(Period).\
            filter(Period.start < (search_date + timedelta(days=1)), Period.end > search_date).all()

        return periods

    def get_periods_by_interval(self, start_date: datetime, finish_date: datetime):
        query = select(Period).where(Period.start.between(start_date, finish_date + timedelta(days=1)) |
                                     Period.end.between(start_date, finish_date + timedelta(days=1)))\
            .order_by(Period.start)
        periods = self.session.scalars(query).all()

        return periods

    @staticmethod
    def _count_period_duration(period: Period, search_date: datetime) -> timedelta:
        start, finish = period.start, period.end
        if not (period.end - period.start).seconds:
            finish = datetime.now()
        if start < search_date:
            start = search_date
        if finish > search_date + timedelta(days=1):
            finish = search_date + timedelta(days=1)

        duration = finish - start
        return duration

    @staticmethod
    def get_date_from_text(text: str) -> datetime | None:
        try:
            date = datetime.strptime(text, "%Y-%m-%d")
        except ValueError:
            date = None

        return date

    def _get_daily_duration(self, duration: timedelta) -> str:
        daily_duration = 'весь день.'
        if not duration.days:
            daily_duration = self._duration_to_human_readable(duration=duration)

        return daily_duration

    @staticmethod
    def _make_zone_stats(duration: timedelta):
        duration_in_seconds = duration.days * 86400 + duration.seconds
        return duration_in_seconds

    @staticmethod
    def _duration_to_human_readable(duration: timedelta) -> str:
        duration_in_seconds = duration.days * 86400 + duration.seconds
        hours: int = duration_in_seconds // 3600
        hours_str = str(hours) + ' год. ' if hours else ''
        minutes: int = duration_in_seconds % 3600 // 60

        return f"{hours_str}{minutes:02} хв."

    @staticmethod
    def _get_emoji():
        return sample("☀🌝🌞⚡✨🔦💡🗿🌟🌈👹🤳⏳🍑⏰🌤🔥🎇🎆", 2)

    @staticmethod
    def _get_light_on_phrase():
        return sample(('сяяли наче новорічна ялинка', 'були зі світлом', 'електрохарчувались',
                    'світились', 'горіли вікна', 'заряджали свої екофлови', 'мали змогу помитися',
                    'сварились в чаті', 'були яскраві', 'були щасливі', 'були з живленням',
                    'мали електроенергію', 'підживлювались', 'були прекрасні'), 2)

    def _get_analytics(self, stats: list[timedelta]) -> str:
        duration_sum = sum(stats, timedelta())
        hr_duration = self._duration_to_human_readable(duration_sum)
        persents = duration_sum / timedelta(days=len(stats)) * 100
        avg = self._duration_to_human_readable(duration_sum / len(stats))
        return f"<b>{hr_duration}</b> ({persents:.1f}%)\n🕙 В середньому по {avg} на добу з електроенергією"
