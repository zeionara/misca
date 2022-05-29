import asyncio
from time import sleep

from telegram import Update
from telegram.ext import Application, ContextTypes, CommandHandler, MessageHandler, filters
from telegram.constants import ParseMode

from .StateManager import StateManager

from .commands import start, stop, subscribe, trace_schedule_for_movie, cancel, set_max_ticket_price, update_max_ticket_price, SETTING_MAX_TICKET_PRICE, make_schedule_message
from .schedule_tracer import trace_schedule
from .utils.collection import make_groups


class TelegramBot:
    def __init__(self, token: str, subscriber_password: str = None, ndays: int = 3, delay: int = 3600):
        self.token = token
        self.subscriber_password = subscriber_password
        self.ndays = ndays
        self.delay = delay

        app = Application.builder().token(token).build()
        notification_app = Application.builder().token(token).build()

        app.add_handler(CommandHandler('start', self.start))
        app.add_handler(CommandHandler('stop', self.stop))
        app.add_handler(CommandHandler('cancel', self.cancel))
        app.add_handler(CommandHandler('set_max_ticket_price', self.set_max_ticket_price))

        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.get_showtimes))

        self.app = app
        self.notification_app = notification_app

        self.state = StateManager()
        self.subscribing_users = set()
        self.sessions = None

    async def get_showtimes(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        subscriber_id = update.effective_chat.id
        text = update.message.text

        if self.subscriber_password is not None and subscriber_id in self.subscribing_users:
            return await subscribe(update, context, self.state, self.subscribing_users, text, subscriber_id, self.subscriber_password)

        if self.subscriber_password is None or self.state.contains_subscriber(subscriber_id):
            if self.subscriber_password is not None and self.state.get_subscriber_state(subscriber_id) == SETTING_MAX_TICKET_PRICE:
                await update_max_ticket_price(update, context, self.state, text, subscriber_id)
                return await self.send_schedule_updates(subscriber_id, self.state.get_max_ticket_price(subscriber_id))

            return await trace_schedule_for_movie(context, self.state, subscriber_id, text, self.sessions)

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

    def run_polling(self):
        self.app.run_polling()

    # async def run_notifications(self):
    #     # asyncio.ensure_future(self._run_notifications())
    #     loop = asyncio.get_event_loop()
    #     loop.create_task(self._run_notifications())
    #     print('sss')

    #     # # await self.app.run_polling()

    #     # while True:
    #     #     print('ok')
    #     #     # self.sessions = tuple(trace_schedule(ndays = self.ndays))

    #     #     # for subscriber_id, max_price in self.state.items:
    #     #     #     sessions_for_subscriber = [session for session in self.sessions if session.satisfies_requirements(max_price = max_price)]
    #     #     #     
    #     #     #     if len(sessions_for_subscriber) > 0:
    #     #     #         self.app.bot.send_message(
    #     #     #             chat_id = subscriber_id,
    #     #     #             text = make_schedule_message(sessions_for_subscriber),
    #     #     #             parse_mode = ParseMode.MARKDOWN
    #     #     #         )

    #     #     #     print(len(self.sessions), len(sessions_for_subscriber))

    #     #     sleep(30)

    async def send_schedule_updates(self, subscriber_id, max_price):
        sessions_for_subscriber = self.state.get_unseen(subscriber_id, [session for session in self.sessions if session.satisfies_requirements(max_price = max_price)])

        print(len(self.sessions), len(sessions_for_subscriber))
        
        if len(sessions_for_subscriber) > 0:
            is_first_group = True

            for group in make_groups(sessions_for_subscriber, group_size = 17):
                await self.notification_app.bot.send_message(
                    chat_id = subscriber_id,
                    text = make_schedule_message(group, include_header = is_first_group, include_movie_name = True),
                    parse_mode = ParseMode.MARKDOWN
                )

                if is_first_group:
                    is_first_group = False

    async def run_notifications(self):
        # loop = asyncio.get_event_loop()
        # await loop.create_task(self.app.run_polling())

        # await self.app.run_polling()

        while True:
            # print('ok')
            self.sessions = tuple(trace_schedule(ndays = self.ndays))

            for subscriber_id, max_price in self.state.items:
                await self.send_schedule_updates(subscriber_id, max_price)
                # sessions_for_subscriber = self.state.get_unseen(subscriber_id, [session for session in self.sessions if session.satisfies_requirements(max_price = max_price)])

                # print(len(self.sessions), len(sessions_for_subscriber))
                # 
                # if len(sessions_for_subscriber) > 0:
                #     is_first_group = True

                #     for group in make_groups(sessions_for_subscriber, group_size = 17):
                #         await self.notification_app.bot.send_message(
                #             chat_id = subscriber_id,
                #             text = make_schedule_message(group, include_header = is_first_group, include_movie_name = True),
                #             parse_mode = ParseMode.MARKDOWN
                #         )

                #         if is_first_group:
                #             is_first_group = False

            sleep(self.delay)
