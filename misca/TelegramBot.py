from telegram import Update
from telegram.ext import Application, ContextTypes, CommandHandler, MessageHandler, filters

from .StateManager import StateManager

from .commands import start, stop, subscribe, trace_schedule_for_movie, cancel, set_max_ticket_price, update_max_ticket_price, SETTING_MAX_TICKET_PRICE


class TelegramBot:
    def __init__(self, token: str, subscriber_password: str = None):
        self.token = token
        self.subscriber_password = subscriber_password

        app = Application.builder().token(token).build()

        app.add_handler(CommandHandler('start', self.start))
        app.add_handler(CommandHandler('stop', self.stop))
        app.add_handler(CommandHandler('cancel', self.cancel))
        app.add_handler(CommandHandler('set_max_ticket_price', self.set_max_ticket_price))

        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.get_showtimes))

        self.app = app

        self.state = StateManager()
        self.subscribing_users = set()

    async def get_showtimes(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        subscriber_id = update.effective_chat.id
        text = update.message.text

        if self.subscriber_password is not None and subscriber_id in self.subscribing_users:
            return await subscribe(update, context, self.state, self.subscribing_users, text, subscriber_id, self.subscriber_password)

        if self.subscriber_password is None or self.state.contains_subscriber(subscriber_id):
            if self.subscriber_password is not None and self.state.get_subscriber_state(subscriber_id) == SETTING_MAX_TICKET_PRICE:
                return await update_max_ticket_price(update, context, self.state, text, subscriber_id)

            return await trace_schedule_for_movie(context, self.state, subscriber_id, text)

        return await context.bot.send_message(
            chat_id = subscriber_id,
            text = 'Please, become a subscriber to get access to the bot features'
        )

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await start(update, context, self.state, self.subscribing_users, self.subscriber_password)

    async def stop(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await stop(update, context, self.state, self.subscribing_users)

    async def cancel(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await cancel(update, context, self.state)

    async def set_max_ticket_price(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await set_max_ticket_price(update, context, self.state)

    def run(self):
        self.app.run_polling()
