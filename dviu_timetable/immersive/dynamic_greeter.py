import random

from dviu_timetable.core.database.user import User

AZIS_MRAZISH_ID = 6274277214


class DynamicGreeter:
    def __init__(self, user: User):
        self._user = user

    def _get_emoji(self) -> str:
        if self._user.user_id == AZIS_MRAZISH_ID:
            return '🤘🏻'
        if self._user.role == 'teacher':
            return '🤝🏻'

        return random.choice(['👋🏻', '🤙🏻'])

    def _get_greeting_text(self) -> str:
        if self._user.role == 'student':
            return 'Привет'
        elif self._user.role == 'teacher':
            return 'Здравствуйте'
        else:
            return 'аъбъа'

    def _get_name(self) -> str:
        if self._user.user_id == AZIS_MRAZISH_ID:
            return random.choice(['Лиза гоголя', 'Азис Мразиш'])

        return self._user.name.split()[0]

    def _get_hint(self) -> str:
        if self._user.user_id == AZIS_MRAZISH_ID:
            return 'Чо шушукаешься?'

        return 'какой-то интересный текст'

    def compose_greeting(self) -> str:
        return (f'{self._get_emoji()} <b>{self._get_greeting_text()}, {self._get_name()}!</b>\n'
                f'{self._get_hint()}')
