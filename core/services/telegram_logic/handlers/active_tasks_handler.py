from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiogram import F
from aiogram.types import Message
from core.services.telegram_logic.callback_data import MainMenuCallback, AcitveTasksCallback
from core.services.database_manager import mantisDatabase
from core.services.telegram_logic.inline_keyboards import InlineButtonsFactory
import asyncio

activeTasksRouter = Router(name="Active Tasks")


@activeTasksRouter.callback_query(MainMenuCallback.filter(
    F.request == "active_tasks"
))
async def handle_active_task_request(query: CallbackQuery):
    taskList = asyncio.to_thread(mantisDatabase.getThisMonthTasks, query.message.chat.id)
    markup = asyncio.to_thread(InlineButtonsFactory.createInlineKeyboard, "Active Tasks", taskList)
    await query.message.answer(
        text="All your tasks from start of the month",
        reply_markup=markup
    )


@activeTasksRouter.callback_query(AcitveTasksCallback.filter(
    F.request == "Back"
))
async def back_button(query: CallbackQuery):
    await query.message.answer(
        text="Back",
        reply_markup=await InlineButtonsFactory.createInlineKeyboard("MainMenu")
    )