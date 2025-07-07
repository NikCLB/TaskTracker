# from core.services.database_manager import mantisDatabase
from aiogram import Dispatcher, types
import asyncio
from conf import config
import logging
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
# from aiogram.fsm.storage.redis import RedisStorage
from core.services.telegram_logic.inline_keyboards import InlineButtonsFactory
from core.services.telegram_logic.handlers.sign_in_handler import signInRouter
from core.services.telegram_logic.handlers.active_tasks_handler import activeTasksRouter
from core.services.telegram_logic.handlers.notification_schedule_handler import NotificationScheduleHandler
from aiogram.fsm.storage.memory import MemoryStorage


# storage = RedisStorage.from_url(
#     f"redis://{config.redis.host}:{config.redis.port}"
# )
storage=MemoryStorage()

dp = Dispatcher(storage=storage)

dp.include_router(signInRouter)
dp.include_router(activeTasksRouter)

@dp.message(CommandStart())
async def handle_start(message: types.Message, state: FSMContext):

    md = await message.answer(
        text="""
        Привет! Этот бот в конце дня будет присылать тебе оповещения с твоими активными задачами.
        Необходимо будет отметить какое кол-во часов ты потратил за текущий день на задачу.
        Если на какой то задаче не поставить кол-во часов, система засчитаеть ноль.
        Так же по кнопке ты сможешь посмотреть свои активные задачи и перевести их в следующий статус по воркфлоу.
        Так же посмотреть статистику с начала месяца
        """,
        reply_markup=await InlineButtonsFactory.createInlineKeyboard("SignIn")
    )

    await message.delete()


async def main():
    logging.basicConfig(level=logging.DEBUG)
    telegramTask = asyncio.create_task(dp.start_polling(config.telegram.bot))
    scheduleNotificationTask = asyncio.create_task(NotificationScheduleHandler().turnOnTaskNotifications())
    config.concurrentTasks.tasks.extend([telegramTask, scheduleNotificationTask])
    try:
        await asyncio.gather(*config.concurrentTasks.tasks)
    except asyncio.CancelledError:
        for task in config.concurrentTasks.tasks:
            task.cancel()
        await asyncio.gather(*config.concurrentTasks.tasks, return_exceptions=True)


if __name__ == "__main__":
    asyncio.run(main())
