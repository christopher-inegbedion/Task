import uuid
import time
from enums.task_type import *
from enums.mode_of_execution import *
from abc import ABC, abstractmethod, abstractproperty


class Task(ABC):
    """Abstract Task class"""

    def __init__(self, name, description):
        # Unique ID for the task
        self.id: uuid.UUID = uuid.uuid3()

        # Name of the task
        self.name: str = name

        # Description of the task
        self.description: str = description

        # UNIX timestamp that represents when the task was created
        self.date_create: int = time.time()

        # The task type
        self.task_type: TaskType = None

        # The stage the task is currently at
        self.stage_status = None

        # The constraint/stage configuration being used by the tasl
        self.constraint_stage_config = None

        # How the task will be provided to the customer
        self.mode_of_execution: ModeOfExecution = None

        # The constraint for the customer to provide compensation for the service/product they recieved. This could be monetary or otherwise.
        self.price_constraint = None

        # A link to the assets used by the task
        self.graphical_assets = None


print(uuid.uuid3())
