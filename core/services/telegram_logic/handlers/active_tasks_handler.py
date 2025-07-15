from aiogram import Router
# from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram import F
# from aiogram.types import Message
from core.services.telegram_logic.callback_data import MainMenuCallback, ActiveTasksCallback
from core.services.database_manager import mantisDatabase
from core.services.telegram_logic.inline_keyboards import InlineButtonsFactory
import asyncio
from conf import ActionType


activeTasksRouter = Router(name="Active Tasks")


@activeTasksRouter.callback_query(MainMenuCallback.filter(
    F.request == "active_tasks"
))
async def handle_active_task_request(query: CallbackQuery):
    taskList = asyncio.to_thread(mantisDatabase.getThisMonthTasks, query.message.chat.id) # type: ignore
    markup = asyncio.to_thread(InlineButtonsFactory.createInlineKeyboard, ActionType.ActiveTasksAction, taskList) # type: ignore
    await query.message.answer( # type: ignore
        text="All your tasks from start of the month",
        reply_markup=markup # type: ignore
    )


@activeTasksRouter.callback_query(ActiveTasksCallback.filter(
    F.request == "Back"
))
async def back_button(query: CallbackQuery):
    await query.message.answer( # type: ignore
        text="Back",
        reply_markup=await InlineButtonsFactory.createInlineKeyboard(ActionType.Back)
    )
