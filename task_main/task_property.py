from abc import ABC, abstractmethod


class TaskProperty(ABC):
    def __init__(self, name,  denoms: list) -> None:
        self.name = name
        self.value = None
        self.denominations = denoms
        self.selected_denom = None

    def set_value(self, value):
        self.value = value

    def set_denom(self, value):
        if value in self.denominations:
            self.selected_denom = value
        else:
            raise Exception(f"Denomination: {value} is not an option")
