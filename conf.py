import os
from dataclasses import dataclass, field
from dotenv import load_dotenv
from sqlalchemy import create_engine, MetaData
from aiogram import Bot
from enum import Enum
from typing import Dict


load_dotenv()

TASK_DAY_TIMES_ROW = None


class ActionType(Enum):
    TrackTasksAction = 1
    ActiveTasksAction = 2
    CustomerMainMenu = 3
    SignIn = 4
    Back = 5


@dataclass
class DatabaseConf:
    host = os.environ.get('DB_HOST')
    port = os.environ.get('DB_PORT')
    databaseName = os.environ.get('DB_NAME')
    username = os.environ.get('DB_USERNAME')
    password = os.environ.get('DB_PASSWORD')
    dbURL = f'mysql+pymysql://{username}:{password}@{host}:{port}/{databaseName}'
    engine = create_engine(dbURL)
    metadata = MetaData()


@dataclass
class CocurrentTasks:
    tasks = []


@dataclass
class TelegramBot:
    token = os.environ.get("TELEGRAM_TOKEN")
    bot = Bot(token=token) # type: ignore


@dataclass
class Redis:
    host = os.environ.get("REDIS_HOST")
    port = os.environ.get("REDIS_PORT")


@dataclass
class Configuration:
    taskHourStorage: Dict[int, Dict[str, Any]]  = field(default_factory=dict) # type: ignore
    telegram = TelegramBot()
    database = DatabaseConf()
    redis = Redis()
    concurrentTasks = CocurrentTasks()

config = Configuration()
