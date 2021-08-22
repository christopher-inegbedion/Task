from task_main.weight_property import WeightProperty
import uuid
import time
from task_main.enums.task_type import *
from task_main.enums.mode_of_execution import *
from abc import ABC
from constraints.constraint_main.constraint import *
from stage.stage import StageGroup


class Task(ABC):
    properties = {
        WeightProperty().name: WeightProperty()
    }

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

        # Task properties
        self.selected_properties = []

    def change_name(self, name):
        self.name = name

    def change_desc(self, desc):
        self.description = desc

    def add_constraint_to_stage(self, constraint, stage_name):
        self.constraint_stage_config._get_stage_with_name(
            stage_name).add_constraint(constraint)

    def add_stage(self, stage):
        self.constraint_stage_config.add_stage(stage)

    def set_constraint_stage_config(self, constraint_config: StageGroup):
        self.constraint_stage_config = constraint_config
        self.current_stage = self.constraint_stage_config.current_stage

    def set_mode_of_execution(self, mode_of_execution: ModeOfExecution):
        self.mode_of_execution = mode_of_execution

    def set_price_constraint(self, price_constraint: Constraint):
        self.price_constraint = price_constraint

    def get_stage_group_details(self):
        return self.constraint_config.get_stage_group_details()

    @classmethod
    def get_available_properties(cls) -> list:
        """Return the names of all the properties"""
        properties = []
        for property in cls.properties:
            properties.append(property)

        return properties

    @classmethod
    def get_property_denominations(cls, name):
        """Return the denomination for a property"""
        if name in cls.properties:
            return cls.properties[name].denominations

        raise Exception(f"Property with name: {name} cannot be found")

    def add_property(self, name: str, value, denom):
        """Add a property to the task"""
        if name in self.properties:
            property = self.properties[name]
            property.value = value
            property.selected_denom = denom
            self.selected_properties.append(
                property
            )
        else:
            raise Exception(f"Property with name: {name} cannot be found")

    def get_selected_properties(self):
        """Return all properties"""
        all_properties = {}
        for property in self.selected_properties:
            all_properties[property.name] = {
                "name": property.name,
                "value": property.value,
                "denomination": property.selected_denom
            }

        return all_properties
