from telegram import Update
from telegram.ext import Application, ContextTypes, CommandHandler, MessageHandler, filters
from telegram.constants import ParseMode

from .schedule_tracer import trace_schedule
from .StateManager import StateManager


class TelegramBot:
    def __init__(self, token: str, subscriber_password: str = None):
        self.token = token
        self.subscriber_password = subscriber_password

        app = Application.builder().token(token).build()

        app.add_handler(CommandHandler('start', self.start))
        app.add_handler(CommandHandler('stop', self.stop))

        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.get_showtimes))

        self.app = app

        self.state = StateManager()
        self.subscribing_users = set()

    async def get_showtimes(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        subscriber_id = update.effective_chat.id
        text = update.message.text

        if self.subscriber_password is not None and subscriber_id in self.subscribing_users:
            if text == self.subscriber_password:
                self.state.add_subscriber(subscriber_id)
                self.subscribing_users.remove(subscriber_id)

                await context.bot.send_message(
                    chat_id = subscriber_id,
                    text = 'The password is correct. You have been added to the list of subscribers'
                )
            else:
                await context.bot.send_message(
                    chat_id = subscriber_id,
                    text = 'The password is incorrect. Please, try again'
                )

            return

        if self.subscriber_password is None or self.state.contains_subscriber(subscriber_id):
            schedule = tuple(trace_schedule(movie = text, ndays = 3))

            if len(schedule) > 0:
                response = "See what I found:\n\n```\n" + '\n'.join(
                    f'{str(session.theater.title):<20} @ {session.room:<20} 📅 {session._date_as_string} ' +
                    f'{"(" + session.time.strftime("%A") + ")":<15} 🕑 {session._time_as_string} 💰 {", ".join(map(str, session.prices))}'
                    for session in schedule
                ) + "\n```"
            else:
                response = "I didn't find anything... Probably the movie is not available, please try a different title"

            await context.bot.send_message(
                chat_id = update.effective_chat.id,
                text = response,
                parse_mode = ParseMode.MARKDOWN
            )
        else:
            await context.bot.send_message(
                chat_id = subscriber_id,
                text = 'Please, become a subscriber to get access to the bot features'
            )

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        subscriber_id = update.effective_chat.id

        if self.state.contains_subscriber(subscriber_id):
            await context.bot.send_message(
                chat_id = update.effective_chat.id,
                text = 'Already subscribed'
            )
        else:
            if self.subscriber_password is None:
                self.state.add_subscriber(subscriber_id)

                await context.bot.send_message(
                    chat_id = update.effective_chat.id,
                    text = 'Hello, I will help you to navigate schedule in the Mirage Cinema theaters. Send me a movie title and I will let you know where you can watch it'
                )
            else:
                await context.bot.send_message(
                    chat_id = subscriber_id,
                    text = 'Hello, please send me the password to start getting updates'
                )

                if subscriber_id not in self.subscribing_users:
                    self.subscribing_users.add(subscriber_id)

    async def stop(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        subscriber_id = update.effective_chat.id

        if not self.state.contains_subscriber(subscriber_id):
            await context.bot.send_message(
                chat_id = update.effective_chat.id,
                text = 'You are not a subscriber'
            )
        else:
            self.state.remove_subscriber(subscriber_id)

            await context.bot.send_message(
                chat_id = update.effective_chat.id,
                text = 'Removed you from the subscribers list'
            )

    def run(self):
        self.app.run_polling()
