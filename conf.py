import os
from dataclasses import dataclass
from dotenv import load_dotenv
from sqlalchemy import create_engine, MetaData
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from aiogram import Bot
from enum import Enum

load_dotenv()

TASK_DAY_TIMES_ROW = None


class ActionType(Enum):
    TrackTasksAction = 1
    ActiveTasksAction = 2
    CustomerMainMenu = 3
    SignIn = 4

@dataclass
class DatabaseConf:
    host = os.environ.get('DB_HOST')
    databaseName = os.environ.get('DB_NAME')
    username = os.environ.get('DB_USERNAME', 'root')
    password = os.environ.get('DB_PASSWORD', 'admin')
    dbURL = f'mysql+pymysql://{username}@localhost/{databaseName}'
    engine = create_engine(dbURL)
    metadata = MetaData()

@dataclass
class CocurrentTasks:
    tasks = []


@dataclass
class TelegramBot:
    token = os.environ.get("TELEGRAM_TOKEN")
    bot = Bot(token=token)


@dataclass
class Redis:
    host = os.environ.get("REDIS_HOST")
    port = os.environ.get("REDIS_PORT")


@dataclass
class Configuration:
    telegram = TelegramBot()
    database = DatabaseConf()
    redis = Redis()
    concurrentTasks = CocurrentTasks()

config = Configuration()
