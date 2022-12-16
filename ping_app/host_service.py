from datetime import datetime

from sqlalchemy import select

from ping_app.db import Session
from ping_app.models import Zone, Host



class HostService:
    def __init__(self, session: Session = Session()):
        self.session = session

    async def add_new_zone(self, zone_name: str) -> Zone:
        new_zone = Zone(name=zone_name)
        await self._add_instance_to_db(instance=new_zone)
        return new_zone

    async def add_new_host(self, hostname: str, address: str, zone_id: int) -> Host:
        new_host = Host(name=hostname, address=address, zone=zone_id)
        await self._add_instance_to_db(instance=new_host)
        return new_host

    async def get_all_hosts(self) -> list[Host]:
        return self.session.scalars(select(Host)).all()

    async def get_all_zones(self) -> list[Zone]:
        return self.session.scalars(select(Zone)).all()

    async def _find_host_by_ip(self, ip_address: str) -> Host:
        query = select(Host).where(Host.address == ip_address)
        result = self.session.scalar(query)
        return result

    async def _add_instance_to_db(self, instance: Host | Zone):
        self.session.add(instance)
        self.session.commit()
        self.session.refresh(instance)

        return instance

    async def invert_online_status(self, instance: Host | Zone):
        instance.is_online = not instance.is_online
        instance.updated_at = datetime.now()
        self.session.commit()

        return instance

    async def delete_host(self, host: Host):
        self.session.delete(host)
        self.session.commit()
        return {'message': f'Host {host.address} was deleted'}


host_crud_service = HostService()
