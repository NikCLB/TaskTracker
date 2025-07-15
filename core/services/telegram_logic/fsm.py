from aiogram.fsm.state import StatesGroup, State


class SignInStates(StatesGroup):
    usernameField = State()
    passwordField = State()


class TasksStates(StatesGroup):
    taskIdField = State()
    taskTimeSpend = State()
