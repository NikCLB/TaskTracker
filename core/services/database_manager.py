from sqlalchemy import Table, select, Engine, CursorResult, update, insert, case
from conf import config
from typing import List
from datetime import datetime, date
from typing import TypeVar, Any, overload, List
from core.services.telegram_logic.fsm import TasksStates
from aiogram.fsm.state import State


_T = TypeVar("_T", bound=Any)

class MantisDatabase:
    def __init__(self):
        self._engine: Engine = config.database.engine
        self._users: Table = Table('mantis_user_table', config.database.metadata, autoload_with=self._engine)
        self._tasksDaytimes: Table = Table('mantis_tasks_daytimes', config.database.metadata, autoload_with=config.database.engine)
        self._condorUserTelegram: Table = Table('mantis_condor_user_telegram', config.database.metadata, autoload_with=config.database.engine)


    def getCondorUsers(self) -> List[CursorResult[_T]]:
        with self._engine.connect() as connection:
            try:
                query = select(self._users).where(self._users.c.username.like("condor.%"))
                result = connection.execute(query)
                return result
            except Exception as e:
                print(f"Ошибка '{e}' при выполнении запроса")


    def getCondorUsersWithTelegram(self) -> List[CursorResult[_T]]:
        with self._engine.connect() as connection:
            try:
                query = select(self._condorUserTelegram).where(self._condorUserTelegram.c.chat_id.is_not(None))
                result = connection.execute(query)
                return result
            except Exception as e:
                print(f"Ошибка '{e}' при выполнении запроса")


    def getCondorUser(self, chat_id: int) -> CursorResult[_T]:
        with self._engine.connect() as connection:
            try:
                query = select(self._condorUserTelegram).where(self._condorUserTelegram.c.chat_id==chat_id)
                result = connection.execute(query)
                return result
            except Exception as e:
                print(f"Ошибка '{e}' при выполнении запроса")


    def insertTelegramChatIDForUser(self, chat_id: int, user_id: int):
        with self._engine.connect() as connection:
            try:
                query = insert(self._condorUserTelegram).values(user_id=user_id, chat_id=chat_id)
                result = connection.execute(query)
                return result
            except Exception as e:
                print(f"Ошибка '{e}' при выполнении запроса")


    def getThisMonthTasks(self) -> List[CursorResult[_T]]:
            first_day_of_month: datetime = datetime(datetime.now().year, datetime.now().month, 1)
            with self._engine.connect() as connection:
                try:
                    query = select(self._tasksDaytimes).where(self._tasksDaytimes.c.date_submitted >= first_day_of_month)
                    result = connection.execute(query)
                    return result
                except Exception as e:
                    print(f"Ошибка '{e}' при выполнении запроса")
    

    def getTodaysNotTrackedTasks(self, dev_id: int) -> List[CursorResult[_T]]:
            with self._engine.connect() as connection:
                current_date = datetime.now().date()
                formatted_date = current_date.strftime("%Y-%m-%d")
                try:
                    query = select(self._tasksDaytimes).where(self._tasksDaytimes.c.last_time_track != formatted_date).where(self._tasksDaytimes.c.dev_id==dev_id)
                    result = connection.execute(query)
                    return result
                except Exception as e:
                    print(f"Ошибка '{e}' при выполнении запроса")


    @overload
    def getThisMonthTasks(self, chat_id: int) -> List[CursorResult[_T]]:
            user = self.getCondorUser(chat_id)
            first_day_of_month: datetime = datetime(datetime.now().year, datetime.now().month, 1)
            with self._engine.connect() as connection:
                try:
                    query = select(self._tasksDaytimes).where(self._tasksDaytimes.c.date_submitted >= first_day_of_month).where(self._tasksDaytimes.c.dev_id==user.user_id)
                    result = connection.execute(query)
                    return result
                except Exception as e:
                    print(f"Ошибка '{e}' при выполнении запроса")


    def insertWorkingHours(self,task_id: int, working_hours: int) -> List[CursorResult[_T]]:
        with self._engine.connect() as connection:
            try:
                query = update(self._tasksDaytimes).where(self._tasksDaytimes.c.id == task_id).values(devs_working_hours=working_hours)
                result = connection.execute(query)
                return result
            except Exception as e:
                print(f"Ошибка '{e}' при выполнении запроса")


    @overload       
    def insertWorkingHours(self, tasksStates: List[State] ) -> List[CursorResult[_T]]:
        with self._engine.connect() as connection:
            try:
                for state in tasksStates:
                        workingHours = state.get_data()
                        query = update(self._tasksDaytimes).where(self._tasksDaytimes.c.id == int(state.state)).values(devs_working_hours=workingHours)
                        connection.execute(query)
            except Exception as e:
                print(f"Ошибка '{e}' при выполнении запроса")

mantisDatabase = MantisDatabase()
