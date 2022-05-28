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


@main.command()
@click.option('--token', '-t', type = str, default = None)
def start(token: str):
    bot = TelegramBot(token)
    bot.run()


if __name__ == '__main__':
    main()
