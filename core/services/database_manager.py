from sqlalchemy import Table, select, Engine, CursorResult, update, insert, or_
from sqlalchemy.engine import Row
from conf import config
from typing import List, Sequence
from datetime import datetime
from typing import TypeVar, Any, overload, List
# from core.services.telegram_logic.fsm import TasksStates
# from aiogram.fsm.state import State


_T = TypeVar("_T", bound=Any)

class MantisDatabase:
    def __init__(self):
        self._engine: Engine = config.database.engine
        self._users: Table = Table('mantis_user_table', config.database.metadata, autoload_with=self._engine)
        self._tasksDaytimes: Table = Table('mantis_tasks_daytimes', config.database.metadata, autoload_with=config.database.engine)
        self._condorUserTelegram: Table = Table('mantis_condor_user_telegram', config.database.metadata, autoload_with=config.database.engine)


    def getCondorUsers(self) -> List[CursorResult[_T]]:
        with self._engine.begin() as connection:
            try:
                query = select(self._users).where(self._users.c.username.like("condor.%"))
                result = connection.execute(query)
                return result
            except Exception as e:
                print(f"Ошибка '{e}' при выполнении запроса")


    def getCondorUsersWithTelegram(self) -> List[CursorResult[_T]]:
        with self._engine.begin() as connection:
            try:
                query = select(self._condorUserTelegram).where(self._condorUserTelegram.c.chat_id.is_not(None))
                result = connection.execute(query)
                return result
            except Exception as e:
                print(f"Ошибка '{e}' при выполнении запроса")


    def getCondorUser(self, chat_id: int) -> Row[Any] | None:
        with self._engine.begin() as connection:
            try:
                query = select(self._condorUserTelegram).where(self._condorUserTelegram.c.chat_id==chat_id)
                result = connection.execute(query)
                return result.fetchone()
            except Exception as e:
                print(f"Ошибка '{e}' при выполнении запроса")


    def _checkExistTelegramChat(self, chat_id: int, user_id: int):
        with self._engine.begin() as connection:
            query = select(self._condorUserTelegram).where(self._condorUserTelegram.c.chat_id==chat_id)
            result = connection.execute(query)
            return result


    def insertTelegramChatIDForUser(self, chat_id: int, user_id: int):
            with self._engine.begin() as connection:
                try:    
                    query = insert(self._condorUserTelegram).values(user_id=user_id, chat_id=chat_id)
                    result = connection.execute(query)
                    return result
                except Exception as e:
                    print(f"Ошибка '{e}' при выполнении запроса")


    def getThisMonthTasks(self) -> List[CursorResult[_T]]:
            first_day_of_month: datetime = datetime(datetime.now().year, datetime.now().month, 1)
            with self._engine.begin() as connection:
                try:
                    query = select(self._tasksDaytimes).where(self._tasksDaytimes.c.date_submitted >= first_day_of_month)
                    result = connection.execute(query)
                    return result
                except Exception as e:
                    print(f"Ошибка '{e}' при выполнении запроса")


    def getTodaysNotTrackedTasks(self, dev_id: int) -> Sequence[Row[Any]] | None:
            with self._engine.begin() as connection:
                current_date = datetime.now().date()
                formatted_date = current_date.strftime("%Y-%m-%d")
                try:
                    query = select(self._tasksDaytimes).where(
                        or_(
                            self._tasksDaytimes.c.last_time_track != formatted_date,
                            self._tasksDaytimes.c.last_time_track.is_(None)
                        ),
                        self._tasksDaytimes.c.dev_id == dev_id,
                        or_(
                            self._tasksDaytimes.c.date_resolved.is_(None),
                            self._tasksDaytimes.c.date_resolved == formatted_date
                        )
                    )
                    result = connection.execute(query)
                    return result.fetchall()
                except Exception as e:
                    print(f"Ошибка '{e}' при выполнении запроса")


    @overload
    def getThisMonthTasks(self, chat_id: int) -> List[CursorResult[_T]]:
            user = self.getCondorUser(chat_id)
            first_day_of_month: datetime = datetime(datetime.now().year, datetime.now().month, 1)
            with self._engine.begin() as connection:
                try:
                    query = select(self._tasksDaytimes).where(self._tasksDaytimes.c.date_submitted >= first_day_of_month).where(self._tasksDaytimes.c.dev_id==user.user_id)
                    result = connection.execute(query)
                    return result
                except Exception as e:
                    print(f"Ошибка '{e}' при выполнении запроса")


    def insertWorkingHours(self, task_id: int, working_hours: int) -> Row[Any]:
        with self._engine.connect() as connection:
            try:
                query = update(self._tasksDaytimes).where(self._tasksDaytimes.c.id == task_id).values(devs_working_hours=working_hours)
                connection.execute(query)
            except Exception as e:
                print(f"Ошибка '{e}' при выполнении запроса")

     
    def insertBatchWorkingHours(self, chat_id: int) -> Row[Any] | None:
        with self._engine.begin() as connection:
            try:
                current_date = datetime.now().date()
                formatted_date = current_date.strftime("%Y-%m-%d")
                for key in config.taskHourStorage[chat_id]["tasks"].keys(): # type: ignore
                    query = update(
                        self._tasksDaytimes
                    ).where(
                        self._tasksDaytimes.c.task_id == key # type: ignore
                    ).values(
                        devs_working_hours=config.taskHourStorage[chat_id]["tasks"][key], # type: ignore
                        last_time_track=formatted_date
                    )
                    connection.execute(query)
            except Exception as e:
                print(f"Ошибка '{e}' при выполнении запроса")

mantisDatabase = MantisDatabase()
