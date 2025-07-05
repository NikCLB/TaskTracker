import pytest
from unittest.mock import AsyncMock, patch
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from core.services.telegram_logic.handlers.sign_in_handler import signInRouter  # Замените на ваш модуль
from core.services.telegram_logic.fsm import SignInStates
from core.services.telegram_logic.inline_keyboards import InlineButtonsFactory
from conf import ActionType


@pytest.mark.asyncio
async def test_handle_sign_in():
    mock_query = AsyncMock(spec=CallbackQuery)
    mock_query.message.answer = AsyncMock()
    mock_query.message.delete = AsyncMock()
    mock_state = AsyncMock(spec=FSMContext)

    await signInRouter.callback_query_handlers[0](mock_query, mock_state)

    mock_query.message.answer.assert_called_once_with(text="Type down your MantisBT username")
    await mock_state.set_state.assert_called_once_with(SignInStates.usernameField)
    await mock_query.message.delete.assert_called_once()

@pytest.mark.asyncio
async def test_ask_for_password():
    mock_message = AsyncMock(spec=Message)
    mock_message.answer = AsyncMock()
    mock_message.delete = AsyncMock()
    mock_state = AsyncMock(spec=FSMContext)

    mock_message.text = "test_username"

    await signInRouter.message_handlers[0](mock_message, mock_state)

    await mock_state.update_data.assert_called_once_with(usernameField="test_username")
    mock_message.answer.assert_called_once_with(text="Type your MantisBT password")
    await mock_state.set_state.assert_called_once_with(SignInStates.passwordField)
    await mock_message.delete.assert_called_once()

@pytest.mark.asyncio
@patch('your_module.SoapClient.makeSignUpRequest', return_value="<response><user_id>123</user_id></response>")
@patch('your_module.XMLManager.parseXMLResponseForID', return_value="123")
@patch('your_module.mantisDatabase.insertTelegramChatIDForUser')
async def test_handle_login(mock_insert, mock_parse, mock_request):
    mock_message = AsyncMock(spec=Message)
    mock_message.answer = AsyncMock()
    mock_message.delete = AsyncMock()
    mock_state = AsyncMock(spec=FSMContext)

    mock_message.text = "test_password"
    mock_message.chat.id = 1

    await mock_state.get_data.return_value = {"usernameField": "test_username"}

    await signInRouter.message_handlers[1](mock_message, mock_state)

    await mock_state.update_data.assert_called_once_with(passwordField="test_password")
    mock_insert.assert_called_once_with(1, "123")
    mock_message.answer.assert_called_once_with(
        text="Личный кабинет",
        reply_markup=await InlineButtonsFactory.createInlineKeyboard(ActionType.CustomerMainMenu)
    )
    await mock_message.delete.assert_called_once()

@pytest.mark.asyncio
@patch('your_module.SoapClient.makeSignUpRequest', return_value="<response><user_id></user_id></response>")
async def test_handle_login_wrong_credentials(mock_request):
    mock_message = AsyncMock(spec=Message)
    mock_message.answer = AsyncMock()
    mock_message.delete = AsyncMock()
    mock_state = AsyncMock(spec=FSMContext)

    mock_message.text = "test_password"
    mock_message.chat.id = 1

    await mock_state.get_data.return_value = {"username"}
