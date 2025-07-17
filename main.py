# from core.services.database_manager import mantisDatabase
from aiogram import Dispatcher, types
import asyncio
from conf import config, ActionType
import logging
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
# from aiogram.fsm.storage.redis import RedisStorage
from core.services.telegram_logic.inline_keyboards import InlineButtonsFactory
from core.services.telegram_logic.handlers.sign_in_handler import signInRouter
from core.services.telegram_logic.handlers.active_tasks_handler import activeTasksRouter
from core.services.telegram_logic.handlers.track_tasks_handler import trackTasksRouter
from core.services.telegram_logic.handlers.notification_schedule_handler import NotificationScheduleHandler
from aiogram.fsm.storage.memory import MemoryStorage


# storage = RedisStorage.from_url(
#     f"redis://{config.redis.host}:{config.redis.port}"
# )
storage=MemoryStorage()

dp = Dispatcher(storage=storage)

dp.include_router(signInRouter)
dp.include_router(activeTasksRouter)
dp.include_router(trackTasksRouter)

@dp.message(CommandStart())
async def handle_start(message: types.Message, state: FSMContext):

    await message.answer(
        text="""
            Hi! Ideally this bot will send you a daily notification with your active tasks at the end of the day.
            BUT
            For now it is not yet implemented
            BUT
            You can do it on your own!
            Go ahead and press button
            You'll need to indicate how many hours you spent on each task for the current day.
            If you don’t enter hours for a task, the system will assume zero.
            By the end press BATCH TRACK and all answers would be uploaded to db.
            Each day it is only one try. Don't fuck up.
            Before BATCH TRACK you can rewrite your values as much as you want.
        """,
        reply_markup=await InlineButtonsFactory.createInlineKeyboard(ActionType.SignIn)
    )

    await message.delete()


async def main():
    logging.basicConfig(level=logging.DEBUG)
    telegramTask = asyncio.create_task(dp.start_polling(config.telegram.bot)) # type: ignore
    # scheduleNotificationTask = asyncio.create_task(NotificationScheduleHandler().turnOnTaskNotifications())
    # config.concurrentTasks.tasks.extend([telegramTask, scheduleNotificationTask]) # type: ignore
    config.concurrentTasks.tasks.append(telegramTask) # type: ignore
    try:
        await asyncio.gather(*config.concurrentTasks.tasks) # type: ignore
    except asyncio.CancelledError:
        for task in config.concurrentTasks.tasks: # type: ignore
            task.cancel() # type: ignore
        await asyncio.gather(*config.concurrentTasks.tasks, return_exceptions=True) # type: ignore


if __name__ == "__main__":
    asyncio.run(main())
