import uuid
import time
from main.enums.task_type import *
from main.enums.mode_of_execution import *
from abc import ABC
from constraints.constraint_main.constraint import *
from main.enums.stage_status import StageStatus
from stage.stage import StageGroup


class Task(ABC):
    """Abstract Task class"""

    def __init__(self, name, description):
        # Unique ID for the task
        self.id: uuid.UUID = uuid.uuid4()

        # Name of the task
        self.name: str = name

        # Description of the task
        self.description: str = description

        # UNIX timestamp that represents when the task was created
        self.date_created: int = time.time()

        # The task type
        self.task_type: TaskType = None

        # The constraint/stage configuration being used by the tasl
        self.constraint_stage_config: StageGroup = None

        # The stage the task is currently at
        self.current_stage: str = None

        # How the task will be provided to the customer
        self.mode_of_execution: ModeOfExecution = None

        # The constraint for the customer to provide compensation for the service/product they recieved. This could be monetary or otherwise.
        self.price_constraint: Constraint = None

        # A link to the assets used by the task
        self.graphical_assets = None

    def change_name(self, name):
        self.name = name

    def change_desc(self, desc):
        self.description = desc

    def set_constraint_stage_config(self, constraint_config: StageGroup):
        self.constraint_stage_config = constraint_config
        self.current_stage = self.constraint_stage_config.current_stage

    def set_mode_of_execution(self, mode_of_execution: ModeOfExecution):
        self.mode_of_execution = mode_of_execution

    def set_price_constraint(self, price_constraint: Constraint):
        self.price_constraint = price_constraint
