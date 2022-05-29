import asyncio
from threading import Thread
import click

from .TelegramBot import TelegramBot
from .schedule_tracer import trace_schedule as trace_schedule_


@click.group()
def main():
    pass


@main.command()
@click.option('--max-price', '-xp', type = int, default = None)
@click.option('--movie', '-m', type = str, default = None)
@click.option('--theater', '-t', type = int, default = None)
@click.option('--ndays', '-n', type = int, default = 0)
def trace_schedule(max_price: int, movie: str, theater: int, ndays: int):
    for session in trace_schedule_(max_price, movie, theater, ndays):
        print(session)


def run_notifications(bot):
    asyncio.run(bot.run_notifications())


@main.command()
@click.option('--token', '-t', type = str)
@click.option('--subscriber-password', '-sp', type = str, default = None)
@click.option('--ndays', '-n', type = int, default = 3)
@click.option('--delay', '-d', type = int, default = 3600)
def start(token: str, subscriber_password: str, ndays: int, delay: int):
    bot = TelegramBot(token, subscriber_password = subscriber_password, ndays = ndays, delay = delay)
    # loop = asyncio.get_event_loop()
    # loop.create_task(bot.run_notifications())
    thread = Thread(target = run_notifications, args = (bot, ))
    thread.start()

    bot.run_polling()


if __name__ == '__main__':
    main()
