from abc import ABC, abstractmethod


class Player(ABC):
    def __init__(self, name, role):
        self.name = name
        self.role = role
        self.alive = True
        self.allies = None

    @abstractmethod
    def vote():
        raise NotImplemented

    @abstractmethod
    def get_message_player(self, state_summary: dict):
        raise NotImplemented

    def update_allies(self, allies):
        self.allies = allies

    def __str__(self):
        return self.name
