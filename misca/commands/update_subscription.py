from telegram import Update
from telegram.ext import ContextTypes

from ..StateManager import StateManager

SETTING_MAX_TICKET_PRICE = 'setting-max-ticket-price'


async def set_max_ticket_price(update: Update, context: ContextTypes.DEFAULT_TYPE, state: StateManager):
    subscriber_id = update.effective_chat.id

    if state.get_subscriber_state(subscriber_id) is None:
        state.set_subscriber_state(subscriber_id, SETTING_MAX_TICKET_PRICE)

        await context.bot.send_message(
            chat_id = subscriber_id,
            text = 'Please, send me the desired max price as an integer number'
        )
    else:
        await context.bot.send_message(
            chat_id = subscriber_id,
            text = 'Cannot start changing max ticket price. Another operation handler is waiting for response'
        )


async def update_max_ticket_price(update: Update, context: ContextTypes.DEFAULT_TYPE, state: StateManager, text: str, subscriber_id: str):
    try:
        value = int(text)
    except:
        await context.bot.send_message(
            chat_id = subscriber_id,
            text = 'Cannot interpret the given value. Please, try again'
        )
    else:
        state.set_max_ticket_price(subscriber_id, value)
        state.set_subscriber_state(subscriber_id, None)

        await context.bot.send_message(
            chat_id = subscriber_id,
            text = 'Updated max ticket price'
        )


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE, state: StateManager):
    subscriber_id = update.effective_chat.id

    if state.get_subscriber_state(subscriber_id) is None:
        await context.bot.send_message(
            chat_id = subscriber_id,
            text = 'There is no pending operation to cancel'
        )
    else:
        state.set_subscriber_state(subscriber_id, None)

        await context.bot.send_message(
            chat_id = subscriber_id,
            text = 'Cancelled the pending operation'
        )
