from typing import Tuple

from .utils.files import read_state_from_yaml_file, write_state_to_yaml_file
from .MovieSession import MovieSession

PATH = 'assets/subscribers.yml'


class StateManager:
    def __init__(self):
        self.subscribers = read_state_from_yaml_file(PATH, default = {})

    def save(self):
        write_state_to_yaml_file(PATH, self.subscribers)

    def contains_subscriber(self, subscriber_id: str):
        return subscriber_id in self.subscribers

    def get_subscriber_state(self, subscriber_id: str):
        if not self.contains_subscriber(subscriber_id):
            raise ValueError(f'User {subscriber_id} is not registered')

        return self.subscribers[subscriber_id].get('state')

    def set_subscriber_state(self, subscriber_id: str, state: str):
        if not self.contains_subscriber(subscriber_id):
            raise ValueError(f'User {subscriber_id} is not registered')

        if state is None:
            self.subscribers[subscriber_id].pop('state')
        else:
            self.subscribers[subscriber_id]['state'] = state

        self.save()

    def set_max_ticket_price(self, subscriber_id: str, value: int):
        if not self.contains_subscriber(subscriber_id):
            raise ValueError(f'User {subscriber_id} is not registered')

        self.subscribers[subscriber_id]['max-ticket-price'] = value
        self.reset_unseen_sessions(subscriber_id)

        self.save()

    def get_max_ticket_price(self, subscriber_id: str):
        if not self.contains_subscriber(subscriber_id):
            raise ValueError(f'User {subscriber_id} is not registered')

        return self.subscribers[subscriber_id].get('max-ticket-price')

    def add_subscriber(self, subscriber_id: str):
        if self.contains_subscriber(subscriber_id):
            raise ValueError(f'User {subscriber_id} is already registered')

        self.subscribers[subscriber_id] = {}

        self.save()

    def remove_subscriber(self, subscriber_id: str):
        if not self.contains_subscriber(subscriber_id):
            raise ValueError(f'User {subscriber_id} is not registered')

        self.subscribers.pop(subscriber_id)

        self.save()

    def get_unseen(self, subscriber_id: str, sessions: Tuple[MovieSession]):
        if not self.contains_subscriber(subscriber_id):
            raise ValueError(f'User {subscriber_id} is not registered')

        seen_session_ids = self.subscribers[subscriber_id].get('seen-sessions')

        if seen_session_ids is None:
            seen_session_ids = [session.id for session in sessions]
            unseen_sessions = sessions
        else:
            unseen_sessions = []
            for session in sessions:
                if session.id not in seen_session_ids:
                    unseen_sessions.append(session)
                    seen_session_ids.append(session.id)

        if len(seen_session_ids) > 0:
            self.subscribers[subscriber_id]['seen-sessions'] = seen_session_ids
            self.save()

        return unseen_sessions

    def reset_unseen_sessions(self, subscriber_id: str):
        if not self.contains_subscriber(subscriber_id):
            raise ValueError(f'User {subscriber_id} is not registered')

        if 'seen-sessions' in self.subscribers[subscriber_id]:
            self.subscribers[subscriber_id].pop('seen-sessions')

    @property
    def items(self):
        for subscriber_id, subscriber in self.subscribers.items():
            yield (subscriber_id, subscriber.get('max-ticket-price'))
