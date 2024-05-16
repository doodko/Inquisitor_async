from random import choice

from bot.types.search_dto import Establishment, SocialContact


class EstablishmentBuilder:
    def __init__(self, establishment: Establishment):
        self.establishment = establishment

    def build_establishment_card(self):
        return (
            self.get_name_string()
            + self.get_description()
            + self.get_address()
            + self.get_work_hours()
            + self.get_phone_numbers()
            + self.get_social_contacts()
        )

    def get_main_icon(self) -> str:
        match self.establishment.category:
            case "store":
                return "🛒"
            case "cafe":
                return "🍽️"
            case "service":
                return "🔤"
            case "finance":
                return "💰"
            case "medicine":
                return "💉"
            case _:
                return "👩‍🔧"

    def get_name_string(self) -> str:
        return f"{self.get_main_icon()} <b>{self.establishment.name}</b>"

    def get_description(self) -> str:
        return self.optional_string(name=self.establishment.description, icon="📃")

    def get_address(self):
        address = self.establishment.address if self.establishment.address else ""
        hint = self.establishment.hint if self.establishment.hint else ""

        if address and hint:
            full_address = f"{address}, {hint}"
            return self.optional_string(name=full_address, icon="📍")
        elif address:
            return self.optional_string(name=address, icon="📍")
        elif hint:
            return self.optional_string(name=hint, icon="📍")
        else:
            return ""

    def get_work_hours(self):
        if not self.establishment.workhrs:
            return ""
        clock_icons = "🕐🕑🕒🕓🕔🕕🕖🕗🕘🕙🕚🕛🕜🕝🕞🕟🕠🕡🕢🕣🕤🕥🕦🕧"

        rows = self.establishment.workhrs.split("|")
        work_hours = [f"{choice(clock_icons)} {row}" for row in rows]
        return "\n" + "\n".join(work_hours)

    def get_phone_numbers(self) -> str:
        if not self.establishment.phone_numbers:
            return ""
        numbers = [f"📞 {number}" for number in self.establishment.phone_numbers]
        return "\n" + "\n".join(numbers)

    def get_social_contacts(self) -> str:
        if not self.establishment.social_contact:
            return ""

        social_contacts = [
            self.contact_format(contact)
            for contact in self.establishment.social_contact
        ]
        contacts_string = "\n🔗 Соцмережі: " + ", ".join(social_contacts)
        return contacts_string

    @staticmethod
    def optional_string(name: str, icon: str = "") -> str:
        return f"\n{icon} {name}" if name else ""

    @staticmethod
    def contact_format(contact: SocialContact):
        mapper = {
            "tg": "телеграм",
            "vb": "вайбер",
            "ig": "інстаграм",
            "web": "сайт",
            "fb": "фейсбук",
        }
        return f"<a href='{contact.value}'>{mapper.get(contact.name)}</a>"
