from telegram import Update
from telegram.ext import ContextTypes

from ..StateManager import StateManager


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE, state: StateManager, subscribing_users: set, subscriber_password: str = None):
    subscriber_id = update.effective_chat.id

    if state.contains_subscriber(subscriber_id):
        await context.bot.send_message(
            chat_id = update.effective_chat.id,
            text = 'Already subscribed'
        )
    else:
        if subscriber_password is None:
            state.add_subscriber(subscriber_id)

            await context.bot.send_message(
                chat_id = update.effective_chat.id,
                text = 'Hello, I will help you to navigate schedule in the Mirage Cinema theaters. Send me a movie title and I will let you know where you can watch it'
            )
        else:
            await context.bot.send_message(
                chat_id = subscriber_id,
                text = 'Hello, please send me the password to start getting updates'
            )

            if subscriber_id not in subscribing_users:
                subscribing_users.add(subscriber_id)


async def subscribe(update: Update, context: ContextTypes.DEFAULT_TYPE, state: StateManager, subscribing_users: set, text: str, subscriber_id: str, subscriber_password: str = None):
    if text == subscriber_password:
        state.add_subscriber(subscriber_id)
        subscribing_users.remove(subscriber_id)

        await context.bot.send_message(
            chat_id = subscriber_id,
            text = 'The password is correct. You have been added to the list of subscribers'
        )
    else:
        await context.bot.send_message(
            chat_id = subscriber_id,
            text = 'The password is incorrect. Please, try again'
        )
