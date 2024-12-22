from abc import ABC, abstractmethod

class Player(ABC):
    def __init__(self, name, role):
        self.name = name
        self.role = role
        self.alive = True

    @abstractmethod
    def vote():
        raise NotImplemented

    @abstractmethod
    def get_message_player(self, state_summary: dict):
        raise NotImplemented
    

    def __str__(self):
        return self.name
