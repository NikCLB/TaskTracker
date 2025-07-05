from aiogram.fsm.state import StatesGroup, State
from typing import List, Any


class SignInStates(StatesGroup):
    usernameField = State()
    passwordField = State()


class TasksStates(StatesGroup):
    def __init__(self, mantisTasksDaytimesRows: List[Any]):
        for task in mantisTasksDaytimesRows:
            setattr(self, task.task_id, State())


class StatesFabric:
    @staticmethod
    async def createTaskStates(self,  mantisTasksDaytimesRows: List[Any] = None) -> TasksStates:
        return TasksStates(mantisTasksDaytimesRows)

    @staticmethod
    async def createSignInStates(self) -> SignInStates:
        return SignInStates
