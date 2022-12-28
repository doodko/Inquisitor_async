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

    def get_periods_by_date(self, start_date: datetime, finish_date: datetime):
        query = select(Period).where(Period.start.between(start_date, finish_date + timedelta(days=1)) |
                                     Period.end.between(start_date, finish_date + timedelta(days=1)))\
            .order_by(Period.start)
        periods = self.session.scalars(query).all()

        return periods

    @staticmethod
    def convert_date_string(datesting: str) -> datetime:
        return datetime.strptime(datesting, "%Y-%m-%d")

    @staticmethod
    def count_period_duration(period: Period, start_date: datetime) -> timedelta:
        if period.start.date() == period.end.date():
            duration = period.end - period.start
        elif period.start.date() == start_date.date():
            duration = start_date + timedelta(days=1) - period.start
        elif period.end.date() == start_date.date():
            duration = period.end - start_date
        else:
            duration = timedelta(0)

        return duration
