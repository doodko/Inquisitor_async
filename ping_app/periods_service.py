from datetime import datetime, timedelta

from loguru import logger
from sqlalchemy import select

from ping_app.db import Session
from ping_app.models import Period, Zone


class PeriodService:
    def __init__(self, session: Session = Session()):
        self.session = session

    def create_new_period(self, zone_id: int,
                          start_time: datetime = datetime.now(),
                          end_time: datetime = datetime.now()):
        new_period = Period(zone=zone_id, start=start_time, end=end_time)
        self.session.add(new_period)
        self.session.commit()

    async def start_stop_period(self, zone: Zone):
        if zone.is_online:
            logger.debug(f"starting new light period in zone {zone.id}")
            new_period = Period(zone=zone.id, start=datetime.now(), end=datetime.now())

            self.session.add(new_period)
            self.session.commit()

        else:
            logger.debug(f"the light period in zone {zone.id} is finished")
            query = select(Period).where(Period.zone == zone.id).order_by(Period.start.desc())
            last_period: Period = self.session.scalar(query)
            last_period.end = datetime.now()

            self.session.commit()

    def calculate_statistics(self, start_date: datetime, finish_date: datetime):
        pass

    def get_periods_by_date(self, search_date: datetime):
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
    def count_period_duration(period: Period, search_date: datetime) -> timedelta:
        start, finish = period.start, period.end
        if not (period.end - period.start).seconds:
            finish = datetime.now()
        if start < search_date:
            start = search_date
        if finish > search_date + timedelta(days=1):
            finish = search_date + timedelta(days=1)

        duration = finish - start
        logger.debug(f"{period.zone} {finish} - {start} = {duration}")
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
