import threading
from constraints.enums.constraint_status import ConstraintStatus
from inventory_main.inventory import Entry
from task_main.enums.mode_of_execution import ModeOfExecution
from stage.stage import Stage, StageGroup
from task_main.product_task import ProductTask
from task_main.enums.task_type import TaskType
from constraints.constraint_main.constraint import Constraint
from task_main.task import Task
import uuid
import time
from task_pipeline.update_abclass import Observer
import asyncio
from constraints.enums.stage_group_status import StageGroupEnum


class Pipeline(Observer):
    def __init__(self, task: Task, constraint_config: StageGroup, display_log=False):
        self.id = str(uuid.uuid4())
        self.date_started = time.time()
        self.current_stage: Stage = None
        self.task = task
        self.constraint_config = constraint_config
        self.all_inputs_passed = []

        self.init_task_for_stages()
        self.set_pipeline_for_stages()

        self.thread_ref = None
        self._display_log = display_log

        # pipeline user information
        self.customer_user_id = None
        self.service_provider_user_id = None

        if self.task == None:
            raise Exception(
                "The task passed to the Pipeline object cannot be null")

        self.stage_log_callback = None
        self.on_update_args = None

        self.stage_complete_callback = None
        self.on_complete_args = None

        self.async_func = False

    def update(self, observer) -> None:
        """Notifies the Stage of a change in the Constraint"""
        if self._display_log:
            print(observer.most_recent_update)

        if self.stage_log_callback is not None:
            self.stage_log_callback(self, self.on_update_args)

        if self.constraint_config.status == StageGroupEnum.COMPLETE:
            self.stage_complete_callback(self, self.on_complete_args)

    def on_update(self, func, *args):
        self.stage_log_callback = func
        self.on_update_args = args

    def on_complete(self, func, *args):
        self.stage_complete_callback = func
        self.on_complete_args = args

    def set_customer_id(self, id):
        self.customer_user_id = id

    def set_provider_id(self, id):
        self.service_provider_user_id = id

    def set_pipeline_for_stages(self):
        for stage in self.constraint_config.stages:
            stage.set_pipeline(self)

    def is_input_req_for_constraint(self, constraint_name, stage_name):
        constraint = self.get_constraint(constraint_name, stage_name)
        return constraint.model.initial_input_required

    def add_input_to_constraint(self, constraint_name, stage_name, input):
        constraint = self.get_constraint(constraint_name, stage_name)
        constraint.add_input(input)
        self.all_inputs_passed.append(input)

    def get_number_of_inputs_required_by_constraints(self, constraint_name, stage_name):
        constraint = self.get_constraint(constraint_name, stage_name)
        return constraint.model.input_count

    def get_constraint(self, constraint_name, stage_name):
        stage = self.get_stage(stage_name)
        constraint = stage.get_constraint(constraint_name)
        return constraint

    def get_stage(self, stage_name):
        return self.constraint_config._get_stage_with_name(stage_name)

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

    def _start(self, stage_name=""):
        self.constraint_config.start(stage_name)

    def start(self, stage_name=""):
        self.thread_ref = threading.Thread(
            target=self._start, args=stage_name)
        self.thread_ref.start()

    def start_stage(self, stage_name):
        self.constraint_config.start(stage_name)

    def abort(self):
        self.constraint_config.stop_all()

    def stop_stage(self, stage_name):
        self.constraint_config.stop_stage(stage_name)

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
