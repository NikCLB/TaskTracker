import aioschedule as schedule
from datetime import datetime, timedelta
import pytz
from core.services.database_manager import mantisDatabase
from core.services.telegram_logic.inline_keyboards import InlineButtonsFactory
import asyncio
from conf import config, TASK_DAY_TIMES_ROW
from core.services.telegram_logic.fsm import StatesFabric


class NotificationScheduleHandler:

    utc_time = "17:30"

    async def _setschedule(self):
        now_utc = datetime.now(pytz.utc)
        job_time = datetime.strptime(self.utc_time, "%H:%M").time()
        job_datetime = now_utc.replace(hour=job_time.hour, minute=job_time.minute, second=0, microsecond=0)
        if job_datetime < now_utc:
            job_datetime += timedelta(days=1)
        schedule.every().day.at(job_datetime.strftime("%H:%M")).do(self._trackTasks)


    async def _trackTasks(self):
        condorUsersWithTelegram = mantisDatabase.getCondorUsersWithTelegram()
        global TASK_DAY_TIMES_ROW 
        for user in condorUsersWithTelegram:
            TASK_DAY_TIMES_ROW = asyncio.to_thread(mantisDatabase.getTodaysNotTrackedTasks, user.user_id)
            inlineKeyboard = asyncio.to_thread(InlineButtonsFactory.createInlineKeyboard, "ActiveTasks", TASK_DAY_TIMES_ROW)
            StatesFabric.createTaskStates()
            await self._sendInlineTasksNotifications(user.chat_id, inlineKeyboard)


    async def _sendInlineTasksNotifications(self,  chat_id, inlineKeyboard):
        config.telegram.bot.send_message(
            chat_id=chat_id,
            text="Нажми на задачу что бы указать затраченное время",
            reply_markup=inlineKeyboard
        )


    async def _checkPendingSchedule(self):
        while True:
            schedule.run_pending()
            asyncio.sleep(1)


    async def turnOnTaskNotifications(self):
        await self._setschedule()
        await self._checkPendingSchedule()
