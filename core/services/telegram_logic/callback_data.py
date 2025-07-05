from aiogram.filters.callback_data import CallbackData


class MainMenuCallback(CallbackData, prefix='main_menu'):
    request: str


class SignInCallback(CallbackData, prefix="sign_in"):
    request: str


class InlineKeyboardCallBack(CallbackData, prefix="inline_keyboards"):
    request: str


class TrackTasksCallBack(CallbackData, prefix="notification_tasks"):
    request: str


class AcitveTasksCallback(CallbackData, prefix="active_tasks"):
    request: str
