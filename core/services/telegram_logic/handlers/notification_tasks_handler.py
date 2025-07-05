from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State
from aiogram.types import CallbackQuery
from aiogram import F
from aiogram.types import Message
from core.services.telegram_logic.fsm import StatesFabric, TasksStates
from core.services.telegram_logic.callback_data import TrackTasksCallBack
from core.services.database_manager import mantisDatabase
from core.services.telegram_logic.inline_keyboards import InlineButtonsFactory
import asyncio
from conf import TASK_DAY_TIMES_ROW, ActionType
from typing import List


trackTasksRouter = Router(name="TrackTasks")

@trackTasksRouter.callback_query(TrackTasksCallBack.filter(
    F.request == "Track"
))
async def sendTrackedTimeToDB(query: CallbackQuery):
    states: List[State]  = [state for state in TasksStates.__dict__.values() if isinstance(state, State)]
    mantisDatabase.insertWorkingHours(states)
    await query.message.answer(
        text="Today's Tasks Tracked",
        reply_markup=await InlineButtonsFactory.createInlineKeyboard(ActionType.CustomerMainMenu)
    )


@trackTasksRouter.callback_query(lambda c: TrackTasksCallBack.filter(c.data))
async def sendRequestToTrackTask(query: CallbackQuery, state: FSMContext):
    await query.message.answer(
        text="Send me an integer ammount of hours spent on that task today." 
    )
    state.update_data(vars(TrackTasksCallBack)[query.data])


@trackTasksRouter.message(state="*")
async def sendRequestToTrackTask(message: Message, state: FSMContext):
    global TASK_DAY_TIMES_ROW 
    current_state = await state.get_state()
    await state.update_data(current_state=message.text)
    await message.answer(
        text="Time Cached. Now move on to track next task. In the end push 'Track' button to save in a Db. Overwise all task would be set to zero",
        reply_markup=await InlineButtonsFactory.createInlineKeyboard(ActionType.TrackTasksAction, TASK_DAY_TIMES_ROW)
    )
