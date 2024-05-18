from enum import StrEnum, auto


class MixpanelEvents(StrEnum):
    REGISTER = auto()
    SEARCH = auto()
    UNSUCCESSFUL_SEARCH = auto()
    VOTE = auto()
    HINT = auto()


class AnswerTypes(StrEnum):
    TOO_SHORT_TEXT = auto()
    TOO_MANY_WORDS = auto()
    ERROR_MESSAGE = auto()
    NO_RESULTS_FOUND = auto()
    SUCCESSFUL_SEARCH = auto()
    POST_INDEX = auto()
    VOTED = auto()
    LIGHT = auto()
