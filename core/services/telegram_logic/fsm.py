from aiogram.fsm.state import StatesGroup, State
from typing import Any, Sequence
from sqlalchemy.engine import Row


class SignInStates(StatesGroup):
    usernameField = State()
    passwordField = State()


class TasksStates(StatesGroup):
    taskIdField = State()
    taskTimeSpend = State()
