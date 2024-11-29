from game.roles import Role
from abc import ABC, abstractmethod

class Player(ABC):
    def __init__(self, name, role: Role):
        self.name = name
        self.role = role
        self.alive = True

    @abstractmethod
    def vote():
        raise NotImplemented

    @abstractmethod
    def write_message():
        raise NotImplemented
    

    def __str__(self):
        return self.name
