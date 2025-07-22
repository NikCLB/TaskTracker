import aioschedule as schedule
from datetime import datetime, timedelta
import pytz
from core.services.database_manager import mantisDatabase
from core.services.telegram_logic.inline_keyboards import InlineButtonsFactory
import asyncio
from conf import config, TASK_DAY_TIMES_ROW, ActionType
from typing import List
from core.services.telegram_logic.handlers.track_tasks_handler import getTodaysUntrackedTasks

class NotificationScheduleHandler:

    utc_time = "18:00"
    tasks_message: str = ""

    async def _setschedule(self):
        now_utc = datetime.now(pytz.utc)
        job_time = datetime.strptime(self.utc_time, "%H:%M").time()
        job_datetime = now_utc.replace(hour=job_time.hour, minute=job_time.minute, second=0, microsecond=0)
        if job_datetime < now_utc:
            job_datetime += timedelta(days=1)
        schedule.every().day.at(job_datetime.strftime("%H:%M")).do(getTodaysUntrackedTasks) # type: ignore


    async def _trackTasks(self):
        condorUsersWithTelegram = await mantisDatabase.getCondorUsersWithTelegram() # type: ignore
        global TASK_DAY_TIMES_ROW 
        for user in condorUsersWithTelegram: # type: ignore
            TASK_DAY_TIMES_ROW = asyncio.to_thread(mantisDatabase.getTodaysNotTrackedTasks, user.user_id) # type: ignore
            inlineKeyboard = asyncio.to_thread(InlineButtonsFactory.createInlineKeyboard, ActionType.ActiveTasksAction, TASK_DAY_TIMES_ROW) # type: ignore
            StatesFabric.createTaskStates() # type: ignore
            await self._sendInlineTasksNotifications(user.chat_id, inlineKeyboard) # type: ignore


    # async def _formTasksMessage(self, dev_id: int):
    #     tasks_names: List[str] = mantisDatabase.getTodaysNotTrackedTasks(dev_id) # type: ignore
    #     for index, task_name in enumerate(tasks_names, start=1):
    #         self.tasks_message += f"{index}: {task_name}\n"


    # async def _sendInlineTasksNotifications(self,  chat_id, inlineKeyboard):
    #     await config.telegram.bot.send_message(
    #         chat_id=chat_id,
    #         text="Нажми на задачу что бы указать затраченное время",
    #         reply_markup=inlineKeyboard
    #     )


    # async def _checkPendingSchedule(self):
    #     while True:
    #         await schedule.run_pending()
    #         await asyncio.sleep(1)


    async def turnOnTaskNotifications(self):
         await self._setschedule()
         ##await self._checkPendingSchedule()
