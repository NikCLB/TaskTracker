from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types.inline_keyboard_markup import InlineKeyboardMarkup
from core.services.telegram_logic.callback_data import SignInCallback, TrackTasksCallBack, ActiveTasksCallback, BackCallBack
from typing import Any, Sequence
from conf import ActionType
from sqlalchemy.engine import Row


class InlineButtonsFactory:
    @staticmethod
    async def createInlineKeyboard(buttonType: ActionType, mantisTasksDaytimesRows: Sequence[Row[Any]] =[]) -> InlineKeyboardMarkup:
        if buttonType == ActionType.TrackTasksAction:
            return await NotificationTasksKeyboard.createInlineKeyboard(mantisTasksDaytimesRows)
        if buttonType == ActionType.ActiveTasksAction:
            return await ActiveTasksKeyboard.createInlineKeyboard(mantisTasksDaytimesRows)
        if buttonType == ActionType.CustomerMainMenu:
            return await MainMenuKeyboard.createInlineKeyboard()
        if buttonType == ActionType.SignIn:
            return await SignInKeyboard.createInlineKeyboard()
        if buttonType == ActionType.Back:
            return await BackKeyborad.createInlineKeyboard()
        else:
            return await EmptyKeyboard.createInlineKeyboard()


class BackKeyborad:
    @staticmethod
    async def createInlineKeyboard() -> InlineKeyboardMarkup:
        inlineKeyboardBuilder = InlineKeyboardBuilder()
        inlineKeyboardBuilder.button(
            text='Back',
            callback_data=TrackTasksCallBack(
                request='back'
            )
        )
        return inlineKeyboardBuilder.as_markup()


class EmptyKeyboard:
    @staticmethod
    async def createInlineKeyboard() -> InlineKeyboardMarkup:
        inlineKeyboardBuilder = InlineKeyboardBuilder()
        inlineKeyboardBuilder.button(
            text='Error',
            callback_data=SignInCallback(
                request='error'
            )
        )
        return inlineKeyboardBuilder.as_markup()

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
            text='Track Tasks',
            callback_data=TrackTasksCallBack(
                request='task_track_start'
            )
        )
        return inlineKeyboardBuilder.as_markup()


class ActiveTasksKeyboard:
    @staticmethod
    async def createInlineKeyboard(mantisTasksDaytimesRows: Sequence[Row[Any]]) -> InlineKeyboardMarkup:
        inlineKeyboardBuilder = InlineKeyboardBuilder()
        for taskRow in mantisTasksDaytimesRows:
            inlineKeyboardBuilder.button(
                text=taskRow.task_name,
                callback_data=ActiveTasksCallback(
                    request=taskRow.id
                )
            )
        inlineKeyboardBuilder.button(
            text="Back",
            callback_data=BackCallBack(
                request="Back"
            )
        ) 
        return inlineKeyboardBuilder.as_markup()        


class NotificationTasksKeyboard:
    @staticmethod
    async def createInlineKeyboard(mantisTasksDaytimesRows: Sequence[Row[Any]]) -> InlineKeyboardMarkup:
        inlineKeyboardBuilder = InlineKeyboardBuilder()
        for taskRow in mantisTasksDaytimesRows:
            inlineKeyboardBuilder.button(
                text=str(taskRow.task_id),
                callback_data=TrackTasksCallBack(
                    request=str(taskRow.task_id)
                )
            )
        inlineKeyboardBuilder.button(
            text="Batch Track",
            callback_data=TrackTasksCallBack(
                request="batch_track"
            )
        )
        inlineKeyboardBuilder.button(
            text="Main Menu",
            callback_data=TrackTasksCallBack(
                request="Menu"
            )
        )
        return inlineKeyboardBuilder.as_markup() 
