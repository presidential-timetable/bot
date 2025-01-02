from aiogram_dialog.widgets.text import Const, Format

from dviu_timetable.bot.main_menu.states import MainMenuState
from aiogram_dialog import Dialog, Window, DialogManager

from dviu_timetable.core.database.user import User

from dviu_timetable.immersive.dynamic_greeter import DynamicGreeter


async def _user_data_getter(dialog_manager: DialogManager, **kwargs):
    user: User = dialog_manager.start_data['user']
    dynamic_greeter = DynamicGreeter(user)

    return {
        'user': user,
        'greeting_text': dynamic_greeter.compose_greeting()
    }


async def make_main_menu_dialog() -> Dialog:
    return Dialog(
        Window(
            Format('{greeting_text}'),
            state=MainMenuState.MAIN,
            getter=_user_data_getter
        )
    )
