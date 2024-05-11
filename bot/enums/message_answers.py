from enum import StrEnum


class MessageAnswers(StrEnum):
    TOO_SHORT_TEXT = "Хто розбере шо тут шукати, напишіть трохи більше букв"
    TOO_MANY_WORDS = "Давайте трохи коротше, спробуйте до трьох слів"
    ERROR_MESSAGE = "Сталась якась халепа, спробуйте пізніше :("
    NO_RESULTS_FOUND = "Мені не вдалось нічого знайти :("
