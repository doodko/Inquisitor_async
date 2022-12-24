from sqlalchemy import select

from ping_app.db import Session
from ping_app.models import User, Subscription


class SubscriptionService:
    def __init__(self, session: Session = Session()):
        self.session = session

    def get_user(self, user_id: int, full_name: str, nickname: str) -> User:
        user = self.session.get(User, user_id)

        if not user:
            user = User(id=user_id, name=full_name, nickname=nickname)
            self.session.add(user)
            self.session.commit()

        return user

    def add_subscription(self, user_id: int, zone_id: int) -> Subscription:
        query = select(Subscription).where(Subscription.user_id == user_id, Subscription.zone_id == zone_id)
        subscription = self.session.scalar(query)

        if not subscription:
            subscription = Subscription(user_id=user_id, zone_id=zone_id)
            self.session.add(subscription)
            self.session.commit()
        return subscription

    def delete_all_user_subscriptions(self, user_id: int):
        query = select(Subscription).where(Subscription.user_id == user_id)
        subscriptions = self.session.scalars(query).all()
        for sub in subscriptions:
            self.session.delete(sub)
            self.session.commit()
