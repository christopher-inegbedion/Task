from constraints.enums.constraint_status import ConstraintStatus
from inventory_main.inventory import Entry
from main.enums.mode_of_execution import ModeOfExecution
from stage.stage import Stage, StageGroup
from main.product_task import ProductTask
from main.enums.task_type import TaskType
from constraints.constraint_main.constraint import Constraint
from main.task import Task
import uuid
import time


class Pipeline:
    def __init__(self, task: Task, constraint_config: StageGroup):
        self.id = uuid.uuid4()
        self.date_started = time.time()
        self.current_stage: Stage = None
        self.task = task
        self.constraint_config = constraint_config

        if self.task == None:
            raise Exception(
                "The task passed to the Pipeline object cannot be null")

        self.init_task_for_stages()

    def init_task_for_stages(self):
        for stage in self.constraint_config.stages:
            self.constraint_config.set_task_for_stage(stage.name, self.task)

    def get_task_name(self):
        return self.task.name

    def get_task_id(self):
        return self.task.id

    def get_task_type(self) -> TaskType:
        return self.task.task_type

    def get_task_creation_date(self) -> int:
        return self.task.date_created

    def get_task_current_stage(self) -> Stage:
        return self.task.current_stage

    def get_task_mode_of_execution(self) -> ModeOfExecution:
        return self.task.mode_of_execution

    def get_entry_from_inventory_for_task(self, entry_index) -> Entry:
        product_task: ProductTask = self.task
        return product_task.inventory.entries[entry_index]

    def get_active_constraint(self) -> Constraint:
        active_constraints = []

        for cnstrt in self.current_stage.constraints:
            if cnstrt.get_status() == ConstraintStatus.ACTIVE:
                active_constraints.append(cnstrt)

        return active_constraints

    def start_constraint(self, stage_name, constraint_name):
        self.constraint_config._get_stage_with_name(stage_name).start_constraint(
            constraint_name)

    def stop_constraint(self, stage_name, constraint_name):
        self.constraint_config._get_stage_with_name(
            stage_name).stop_constraint(constraint_name)

    def start(self, stage_name=""):
        self.constraint_config.start(stage_name)

    def start_stage(self, stage_name):
        self.constraint_config.start(stage_name)

    def stop_stage(self, stage_name):
        pass

    def pause_stage(self):
        self.current_stage.freeze()

    def log(self):
        print("----------------")
        print(
            f"--Task details--")
        print("----------------")
        print(
            f">>task name: {self.task.name}, task description: {self.task.description}")
        print(f">>task id: {self.task.id}")
        print(f">>task type: {self.task.task_type}")
        print(f">>time created: {self.task.date_created}")
        print(f">>task current stage: {self.task.current_stage}")
        print(f">>task mode of execution: {self.task.mode_of_execution}")

        if self.task.task_type == TaskType.PRODUCT:
            product_task: ProductTask = self.task
            product_task.inventory.log()

        print("\n--Task's Constraint/Stage configuration--")
        for stage in self.constraint_config.stages:
            print(f"STAGE name: {stage.name}")
            for cnstrt in stage.constraints:
                print(f"\t>>CONSTRAINT name: {cnstrt.name}")
            print()
