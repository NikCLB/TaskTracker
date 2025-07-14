from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from conf import config
from aiogram import F
import asyncio
from core.services.telegram_logic.fsm import TasksStates
from aiogram.types import Message
from core.services.telegram_logic.callback_data import TrackTasksCallBack
from core.services.database_manager import mantisDatabase
from core.services.telegram_logic.inline_keyboards import InlineButtonsFactory
from conf import ActionType
from typing import Any, Sequence
from sqlalchemy.engine import Row


trackTasksRouter = Router(name="TrackTasks")


@trackTasksRouter.callback_query(TrackTasksCallBack.filter(
    F.request == "Menu"
))
async def backToMenu(query: CallbackQuery): # type: ignore
    await query.message.answer( # type: ignore
        text="Main menu",
        reply_markup=await InlineButtonsFactory.createInlineKeyboard(ActionType.CustomerMainMenu)
    )


@trackTasksRouter.callback_query(TrackTasksCallBack.filter(
    F.request == "Track"
))
async def backToMenu(query: CallbackQuery):
    await asyncio.to_thread(mantisDatabase.insertWorkingHours)
    await query.message.answer( # type: ignore
        text="All tasks have been tracked succesfully. Now back to main menu",
        reply_markup=await InlineButtonsFactory.createInlineKeyboard(ActionType.CustomerMainMenu)
    )


@trackTasksRouter.callback_query(TrackTasksCallBack.filter(
    F.request == "task_track_start"
))
async def getTodaysUntrackedTasks(query: CallbackQuery):
    chat_id: int = query.message.chat.id # type: ignore
    currentUserRow: Row[Any] | None =  await asyncio.to_thread(mantisDatabase.getCondorUser, chat_id)
    if currentUserRow is not None:
        todaysUserTasksRows: Sequence[Row[Any]] =  await asyncio.to_thread(
            mantisDatabase.getTodaysNotTrackedTasks, currentUserRow[1]
        ) # type: ignore
        if len(todaysUserTasksRows) != 0:
            config.taskMessage = ""
            for taskRow in todaysUserTasksRows:
                config.taskMessage += f"{taskRow.task_id}: {taskRow.task_name}\n"
            config.taskInlineKeyboard = await InlineButtonsFactory.createInlineKeyboard(
                ActionType.TrackTasksAction, todaysUserTasksRows
            )
            await query.message.answer( # type: ignore
                text=config.taskMessage,
                reply_markup=config.taskInlineKeyboard
            )
        else:
            await query.message.answer( # type: ignore
                text="No Untracked tasks for today",
                reply_markup=await InlineButtonsFactory.createInlineKeyboard(
                    ActionType.CustomerMainMenu
                )
            )
    else:
        await query.message.answer( # type: ignore
                text="Couldn't find you in DB",
                reply_markup= await InlineButtonsFactory.createInlineKeyboard(
                    ActionType.CustomerMainMenu
                )
            )


@trackTasksRouter.callback_query(lambda c: TrackTasksCallBack.filter(c.data)) # type: ignore
async def sendRequestToTrackTask(query: CallbackQuery, state: FSMContext): # type: ignore
    data = TrackTasksCallBack.unpack(query.data) # type: ignore
    await state.set_state(TasksStates.taskIdField)
    await state.update_data(taskIdField=data.request)
    await state.set_state(TasksStates.taskTimeSpend)
    await query.message.answer( # type: ignore
        text="Send me an integer ammount of hours spent on that task today.",
        reply_markup= await InlineButtonsFactory.createInlineKeyboard(
            ActionType.CustomerMainMenu
        )
    ) # type: ignore


@trackTasksRouter.message(TasksStates.taskTimeSpend)
async def saveTimeSpend(
    message: Message,
    state: FSMContext
):
    await state.update_data(taskTimeSpend=message.text)
    data = await state.get_data()
    config.dailyTaskHourStorage[data["taskIdField"]] = data["taskTimeSpend"] # type: ignore
    await message.answer(
        text=config.taskMessage,
        reply_markup=config.taskInlineKeyboard
    )
