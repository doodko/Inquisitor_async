from datetime import datetime, timedelta
from random import choice, sample

from loguru import logger
from sqlalchemy import select

from ping_app.db import Session
from ping_app.models import Period, ElectricityAvailability


class StatisticsService:
    def __init__(self, session: Session = Session()):
        self.session = session

    def make_stats_message(self, date: datetime) -> str:
        stats = self.get_daily_stats(date=date)
        emoji = sample("🕓🕙🕝⚡✨🔦💡🗿🌟🌈👹🤳⏳🍑⏰🌤🔥🎇🎆", 2)
        light_on = sample(('сяяли наче новорічна ялинка', 'були зі світлом', 'електрохарчувались',
                    'світились', 'горіли вікна', 'заряджали свої екофлови', 'мали змогу помитися',
                    'сварились в чаті', 'були яскраві', 'були щасливі', 'були з живленням',
                    'мали електроенергію', 'підживлювались', 'були прекрасні'), 2)

        message = f"Спостереження за <b>{stats.date}</b>:\n" \
                  f"{emoji[0]} Перші лінії {light_on[0]} <b>{self.timedelta_to_human_readable(stats.zone1_duration)}</b>\n" \
                  f"{emoji[1]} ЛУ/Соборна {light_on[1]} <b>{self.timedelta_to_human_readable(stats.zone2_duration)}</b>"

        message += "\n\nЦікавить інша дата? Введіть команду в такому форматі:\n/stats <i>РРРР-ММ-ДД</i>"

        return message

    def create_daily_stats(self, date: datetime) -> ElectricityAvailability:
        zone1_duration, zone2_duration = self._calculate_daily_stats(date=date)
        new_stats = ElectricityAvailability(date=date, zone1_duration=zone1_duration, zone2_duration=zone2_duration)

        self.session.add(new_stats)
        self.session.commit()

        return new_stats

    def get_daily_stats(self, date: datetime) -> ElectricityAvailability:
        stats = self.session.scalar(select(ElectricityAvailability).where(ElectricityAvailability.date == date.date()))
        if not stats:
            stats = self.create_daily_stats(date=date)
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
    def get_date_period_from_message(text: str) -> tuple[datetime, datetime]:
        yesterday = datetime.today() - timedelta(days=1)

        def convert_string_to_date_or_yesterday(sting: str) -> datetime:
            try:
                return datetime.strptime(sting, "%Y-%m-%d")
            except ValueError:
                return yesterday

        start_date = finish_date = yesterday
        if len(text.split()) == 2:
            start_date = finish_date = convert_string_to_date_or_yesterday(text.split()[1])
        if len(text.split()) == 3:
            start_date = convert_string_to_date_or_yesterday(text.split()[1])
            finish_date = convert_string_to_date_or_yesterday(text.split()[2])

        return start_date, finish_date

    @staticmethod
    def timedelta_to_human_readable(tmdlt: timedelta) -> str:
        human_readable = 'весь день.'
        if not tmdlt.days:
            tmdlt_in_seconds = tmdlt.seconds
            hours: int = tmdlt_in_seconds // 3600
            hours_str = str(hours) + ' год. ' if hours else ''
            minutes: int = tmdlt_in_seconds % 3600 // 60

            human_readable = f"{hours_str}{minutes:02} хв."

        return human_readable
