from aiogram import Router
from aiogram.types import CallbackQuery
import asyncio
from aiogram import F
from core.services.telegram_logic.callback_data import SignInCallback
from aiogram.fsm.context import FSMContext
from core.services.telegram_logic.fsm import SignInStates
from aiogram.types import Message
from core.services.soap_manager import soapClient
from core.services.xml_manager import xmlManager
from core.services.database_manager import mantisDatabase
from core.services.telegram_logic.inline_keyboards import InlineButtonsFactory
from conf import ActionType


signInRouter = Router(name="Sign In")

@signInRouter.callback_query(SignInCallback.filter(
    F.request == "sign_in"
))
async def handle_sign_in(query: CallbackQuery, state: FSMContext) -> None:
    await query.message.answer(
        text="Type down your MantisBT username"
    )
    await state.set_state(SignInStates.usernameField)
    await query.message.delete()


@signInRouter.message(SignInStates.usernameField)
async def ask_for_password(
    message: Message,
    state: FSMContext
) -> None:
    await state.update_data(usernameField=message.text)
    await message.answer(
        text="Type your MantisBT password"
    )
    await state.set_state(SignInStates.passwordField)
    await message.delete()


@signInRouter.message(SignInStates.passwordField)
async def handleLogin(
    message: Message,
    state: FSMContext
) -> None:
    await state.update_data(passwordField=message.text)
    data = await state.get_data()
    username = data.get("usernameField")
    password = data.get("passwordField")
    response = await asyncio.to_thread(soapClient.makeSignUpRequest, username, password)
    user_id: str = await asyncio.to_thread(xmlManager.parseXMLResponseForID, response)
    if user_id is None:
        await message.answer(
            text="Wrong credentials",
            reply_markup=await InlineButtonsFactory.createInlineKeyboard(ActionType.SignIn)
        )
        await message.delete()
        return
    chat_id: int = message.chat.id
    asyncio.to_thread(mantisDatabase.insertTelegramChatIDForUser, chat_id, user_id)
    await message.answer(
        text="Личный кабинет",
        reply_markup=await InlineButtonsFactory.createInlineKeyboard(ActionType.CustomerMainMenu)
    )
    await message.delete()
