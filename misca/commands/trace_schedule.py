from telegram.ext import ContextTypes
from telegram.constants import ParseMode

from ..schedule_tracer import trace_schedule


async def trace_schedule_for_movie(context: ContextTypes.DEFAULT_TYPE, subscriber_id: str, title: str):
    schedule = tuple(trace_schedule(movie = title, ndays = 3))

    if len(schedule) > 0:
        response = "See what I found:\n\n```\n" + '\n'.join(
            f'{str(session.theater.title):<20} @ {session.room:<20} 📅 {session._date_as_string} ' +
            f'{"(" + session.time.strftime("%A") + ")":<15} 🕑 {session._time_as_string} 💰 {", ".join(map(str, session.prices))}'
            for session in schedule
        ) + "\n```"
    else:
        response = "I didn't find anything... Probably the movie is not available, please try a different title"

    await context.bot.send_message(
        chat_id = subscriber_id,
        text = response,
        parse_mode = ParseMode.MARKDOWN
    )
