from telegram import Update
from telegram.ext import ContextTypes

from ..StateManager import StateManager


async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE, state: StateManager, subscribing_users: set):
    subscriber_id = update.effective_chat.id

    if not state.contains_subscriber(subscriber_id):
        if subscriber_id in subscribing_users:
            subscribing_users.remove(subscriber_id)

            await context.bot.send_message(
                chat_id = update.effective_chat.id,
                text = 'Stopped attempting to subscribe'
            )

            return

        await context.bot.send_message(
            chat_id = update.effective_chat.id,
            text = 'You are not a subscriber'
        )
    else:
        state.remove_subscriber(subscriber_id)

        await context.bot.send_message(
            chat_id = update.effective_chat.id,
            text = 'Removed you from the subscribers list'
        )
