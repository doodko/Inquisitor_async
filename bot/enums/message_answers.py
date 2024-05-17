from enum import StrEnum, auto
from random import choice


class AnswerTypes(StrEnum):
    TOO_SHORT_TEXT = auto()
    TOO_MANY_WORDS = auto()
    ERROR_MESSAGE = auto()
    NO_RESULTS_FOUND = auto()
    SUCCESSFUL_SEARCH = auto()
    POST_INDEX = auto()
    VOTED = auto()
    LIGHT = auto()


class MessageAnswers:
    dtek = "<a href='https://t.me/DTEKKyivRegionElektromerezhiBot'>ДТЕК</a>"

    too_short_text = [
        "Будь ласка, напишіть більше деталей.",
        "Трохи більше інформації буде корисною.",
        "Можливо, трохи деталізувати?",
        "Потрібно трохи більше інформації.",
        "Додайте трошки контексту, будь ласка.",
    ]
    too_many_words = [
        "Спробуйте сформулювати коротше. До трьох слів.",
        "Можливо, скоротити трохи текст? 1-2 слова буде достатньо.",
        "Занадто багато слів, спробуйте стиснути.",
        "Многа букав ніасіліл.",
    ]
    error_message = [
        "Сталась якась халепа, спробуйте пізніше :(",
        "Вибачте, сталася помилка, спробуйте знову пізніше :(",
        "На жаль, щось пішло не так, спробуйте пізніше :(",
        "Помилка, спробуйте пізніше або зверніться за допомогою.",
        "Щось пішло не так, спробуйте знову трохи пізніше :(",
        "На жаль, виникла помилка, спробуйте інший запит :(",
    ]
    no_results_found = [
        "На жаль, нічого не знайдено за вашим запитом :(",
        "Результатів немає, спробуйте змінити запит.",
        "По вашому запиту нічого не знайдено.",
        "Мені не вдалось нічого знайти :(",
        "Пошук не дав результатів, спробуйте інший запит.",
    ]
    successful_search = [
        "Все що вдалося знайти:",
        "Ваші результати пошуку:",
        "Пошукав, ось результати:",
        "Таке знайшлося:",
        "Ось шо я знайшов, підійде?",
        "Ось це можу запропонувати:",
    ]
    post_index = [
        "08148",
        "з ранку був 08148",
        "досі 08148",
        "не повірите, але все ще 08148",
        "08148, якщо мені не зраджує пам'ять",
        "нуль вісім сто сорок вісім",
    ]
    voted = [
        "Штош, так і запишемо!",
        "Підтримую ваш вибір.",
        "Теж так би проголосував, якшочесно..",
        "Зробив би так само, але в мене лапки!",
        "Не всі з вами погодяться!",
        "Так народжувалась демократія.",
        "Окей, записав.",
        "Гадаю, це взаємно",
    ]
    light = [
        f"Я вже давно не слідкую за світлом, з цим краще справляється {dtek}",
        f"Ці питання я делегував коллегам з {dtek}",
        f"Гадаю, {dtek} краще знає",
        f"Запитайте це у {dtek}, будь ласка",
        f"У {dtek} питали?",
        f"Я знаю де вінішка купити чи бургер замовити, а це краще до {dtek} направити :)",
    ]

    @classmethod
    def answer(cls, answer_type):
        if hasattr(cls, answer_type):
            answer_list = getattr(cls, answer_type)
            return choice(answer_list)
