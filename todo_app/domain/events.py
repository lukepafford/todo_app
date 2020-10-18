from dataclasses import dataclass


class Event:
    pass


@dataclass
class TodoSaved(Event):
    todo_id: int
