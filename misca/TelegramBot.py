from telegram import Update
# from telegram import Bot  # , CallbackContext, CommandHandler
from telegram.ext import Application, ContextTypes, CommandHandler, MessageHandler, filters
from telegram.constants import ParseMode

from .schedule_tracer import trace_schedule




class TelegramBot:
    def __init__(self, token: str):
        self.token = token
        # app = Bot(token)
        app = Application.builder().token(token).build()

        app.add_handler(CommandHandler('start', self.start))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.get_showtimes))

        self.app = app

    async def get_showtimes(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        text = update.message.text

        schedule = tuple(trace_schedule(movie = text, ndays = 3))

        if len(schedule) > 0:
            response = "See what I found:\n\n```\n" + '\n'.join(
                f'{str(session.theater.title):<20} @ {session.room:<20} 📅 {session._date_as_string} {"(" + session.time.strftime("%A") + ")":<15} 🕑 {session._time_as_string} 💰 {", ".join(map(str, session.prices))}'
                for session in schedule
            ) + "\n```"
        else:
            response = "I didn't find anything... Probably the movie is not available, please try a different title"

        await context.bot.send_message(
            chat_id = update.effective_chat.id,
            text = response,
            parse_mode = ParseMode.MARKDOWN
        )

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await context.bot.send_message(
            chat_id = update.effective_chat.id,
            text = 'Hello, I will help you to navigate schedule in the Mirage Cinema theaters. Send me a movie title and I will let you know where you can watch it'
        )

    def run(self):
        self.app.run_polling()
        # print(dir(self.app))
        # for update in self.app.get_updates():
        #     self.app.send_message(chat_id = update.effective_chat.id, text = 'hello')
        #     print(dir(update))
        #     # print(dir(update.effective_chat.id))
        # # with self.app:
        # # print((self.app.get_updates())[0])
        # # self.app.run_polling()
