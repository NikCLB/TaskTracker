from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types.inline_keyboard_markup import InlineKeyboardMarkup
from core.services.telegram_logic.callback_data import MainMenuCallback, SignInCallback, TrackTasksCallBack, AcitveTasksCallback
from typing import List, Any
from conf import ActionType


class InlineButtonsFactory:
    @staticmethod
    async def createInlineKeyboard(buttonType: str, mantisTasksDaytimesRows: List[Any] = None):
        if buttonType == ActionType.TrackTasksAction:
            return await NotificationTasksKeyboard.createInlineKeyboard(mantisTasksDaytimesRows)
        if buttonType == ActionType.ActiveTasksAction:
            return await ActiveTasksKeyboard.createInlineKeyboard(mantisTasksDaytimesRows)
        if buttonType == ActionType.CustomerMainMenu:
            return await MainMenuKeyboard.createInlineKeyboard()
        if buttonType == ActionType.SignIn:
            return await SignInKeyboard.createInlineKeyboard()


class SignInKeyboard:
    @staticmethod
    async def createInlineKeyboard() -> InlineKeyboardMarkup:
        inlineKeyboardBuilder = InlineKeyboardBuilder()
        inlineKeyboardBuilder.button(
            text='Sign In',
            callback_data=SignInCallback(
                request='sign_in'
            )
        )
        return inlineKeyboardBuilder.as_markup()


class MainMenuKeyboard:
    @staticmethod
    async def createInlineKeyboard() -> InlineKeyboardMarkup:
        inlineKeyboardBuilder = InlineKeyboardBuilder()

        inlineKeyboardBuilder.button(
            text='Текущие задачи',
            callback_data=MainMenuCallback(
                request='active_tasks'
            )
        )

        inlineKeyboardBuilder.button(
            text='Статистика за месяц',
            callback_data=MainMenuCallback(
                request='month_stats'
            )
        )
        inlineKeyboardBuilder.adjust(1, 1)
        return inlineKeyboardBuilder.as_markup()


class ActiveTasksKeyboard:
    @staticmethod
    async def createInlineKeyboard(mantisTasksDaytimesRows: List[Any]) -> InlineKeyboardMarkup:
        inlineKeyboardBuilder = InlineKeyboardBuilder()
        for taskRow in mantisTasksDaytimesRows:
            inlineKeyboardBuilder.button(
                text=taskRow.task_name,
                callback_data=AcitveTasksCallback(
                    request=taskRow.id
                )
            )
        inlineKeyboardBuilder.button(
            text="Back",
            callback_data=AcitveTasksCallback(
                request="Back"
            )
        ) 
        return inlineKeyboardBuilder.as_markup()        


class NotificationTasksKeyboard:
    @staticmethod
    async def createInlineKeyboard(mantisTasksDaytimesRows: List[Any]) -> InlineKeyboardMarkup:
        inlineKeyboardBuilder = InlineKeyboardBuilder()
        for taskRow in mantisTasksDaytimesRows:
            inlineKeyboardBuilder.button(
                text=taskRow.task_name,
                callback_data=TrackTasksCallBack(
                    request=taskRow.id
                )
            )
        inlineKeyboardBuilder.button(
            text="Track",
            callback_data=TrackTasksCallBack(
                request="Track"
            )
        )
        return inlineKeyboardBuilder.as_markup() 
