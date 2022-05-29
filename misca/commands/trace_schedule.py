from typing import Tuple

from telegram.ext import ContextTypes
from telegram.constants import ParseMode

from ..StateManager import StateManager
# from ..schedule_tracer import trace_schedule
from ..MovieSession import MovieSession
from ..utils.string import truncate


def make_schedule_message(schedule: Tuple[MovieSession], include_header: bool = True, include_movie_name: bool = False):
    return ("See what I found:\n\n```\n" if include_header else "```\n") + '\n'.join(
        (f'{truncate(str(session.title), 15):<15} 🌎 ' if include_movie_name else '') +
        f'{truncate(str(session.theater.title), 15):<15} @ {truncate(session.room, 10):<10} 📅 {session._date_as_string} ' +
        f'{"(" + truncate(session.time.strftime("%A"), 8) + ")":<10} 🕑 {session._time_as_string} 💰 {", ".join(map(str, session.prices))}'
        for session in schedule
    ) + "\n```"


async def trace_schedule_for_movie(context: ContextTypes.DEFAULT_TYPE, state: StateManager, subscriber_id: str, title: str, sessions: Tuple[MovieSession]):
    # schedule = tuple(trace_schedule(movie = title, max_price = state.get_max_ticket_price(subscriber_id), ndays = 3))
    schedule = [session for session in sessions if session.satisfies_requirements(movie = title, max_price = state.get_max_ticket_price(subscriber_id))]

    if len(schedule) > 0:
        response = make_schedule_message(schedule)
    else:
        response = "I didn't find anything... Probably the movie is not available, please try a different title"

    await context.bot.send_message(
        chat_id = subscriber_id,
        text = response,
        parse_mode = ParseMode.MARKDOWN
    )
