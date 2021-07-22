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
from constraints.enums.stage_status import StageStatus


class Pipeline(Observer):
    def __init__(self, task: Task, stage_group: StageGroup, display_log=False):
        # Identifies the Pipelie
        self.id = str(uuid.uuid4())

        # Keeps track of when the pipeline started
        self.date_started = time.time()

        # The current stage of the pipeline instance
        self.current_stage: Stage = None

        # The task with the current pipeline instance
        self.task = task

        # The stage group stores all the stages
        self.stage_group = stage_group

        self.thread_ref = None

        # Describes if the Pipeline should display log messages
        self._display_log = display_log

        # pipeline user information
        self.customer_user_id = None
        self.service_provider_user_id = None

        self.stage_log_callback = None
        self.on_update_args = None

        self.pipeline_complete_callback = None
        self.on_complete_args = None

        self.waiting_for_specific_stage = False
        self.specific_stage_update_name = ""
        self.specific_stage_callback = None
        self.specific_stage_args = None

        self.waiting_for_specific_constraint = False
        self.on_constraint_complete_constraint_name = ""
        self.specific_constraint_callback = None
        self.specific_constraint_args = None

        self.async_func = False

        # A task has to be passed to the Pipeline
        if self.task == None:
            raise Exception(
                "The task passed to the Pipeline object cannot be null")

        self.init_task_for_stages()
        self.set_pipeline_for_stages()

    def update(self, observer) -> None:
        """Notifies the Stage of a change in the Constraint"""
        most_recent_update = observer.most_recent_update

        if self._display_log:
            print(observer.most_recent_update)

        if self.specific_stage_callback is not None:
            if most_recent_update["event"] == StageStatus.COMPLETE:
                if self.waiting_for_specific_stage:
                    if most_recent_update["value"] == self.specific_stage_update_name:
                        self.specific_stage_callback(
                            self, self.specific_stage_args)
                else:
                    self.specific_stage_callback(
                        self, self.specific_stage_args)

        if self.specific_constraint_callback is not None:
            if most_recent_update["event"] == StageStatus.CONSTRAINT_COMPLETED:
                if self.waiting_for_specific_constraint:
                    if most_recent_update["value"]["name"] == self.on_constraint_complete_constraint_name:
                        self.specific_constraint_callback(
                            self, self.specific_constraint_args)
                else:
                    self.specific_constraint_callback(
                        self, self.specific_constraint_args)

        if self.stage_log_callback is not None:
            self.stage_log_callback(self, self.on_update_args)

        if self.pipeline_complete_callback is not None:
            if self.stage_group.status == StageGroupEnum.COMPLETE:
                self.pipeline_complete_callback(self, self.on_complete_args)

    def on_update(self, func, *args):
        self.stage_log_callback = func
        self.on_update_args = args

    def on_stage_complete(self, func, *args, stage_name="",):
        if stage_name == "":
            self.waiting_for_specific_stage = False
        else:
            self.waiting_for_specific_stage = True
            self.specific_stage_update_name = stage_name

        self.specific_stage_callback = func
        self.specific_stage_args = args

    def on_complete(self, func, *args):
        self.pipeline_complete_callback = func
        self.on_complete_args = args

    def on_constraint_complete(self, func, *args, constraint_name=""):
        if constraint_name == "":
            self.waiting_for_specific_constraint = False
        else:
            self.waiting_for_specific_constraint = True
            self.on_constraint_complete_constraint_name = constraint_name

        self.specific_constraint_callback = func
        self.specific_constraint_args = args

    def set_customer_id(self, id):
        self.customer_user_id = id

    def set_provider_id(self, id):
        self.service_provider_user_id = id

    def set_pipeline_for_stages(self):
        for stage in self.stage_group.stages:
            stage.set_pipeline(self)

    def is_input_req_for_constraint(self, constraint_name, stage_name):
        constraint = self.get_constraint(constraint_name, stage_name)
        return constraint.model.initial_input_required

    def add_input_to_constraint(self, constraint_name, stage_name, input):
        constraint = self.get_constraint(constraint_name, stage_name)
        constraint.add_input(input)

    def get_number_of_inputs_required_by_constraints(self, constraint_name, stage_name):
        constraint = self.get_constraint(constraint_name, stage_name)
        return constraint.model.input_count

    def get_constraint(self, constraint_name, stage_name):
        stage = self.get_stage(stage_name)
        constraint = stage.get_constraint(constraint_name)
        return constraint

    def get_stage(self, stage_name):
        return self.stage_group._get_stage_with_name(stage_name)

    def get_stage_group_details(self):
        return self.stage_group.get_stage_group_details()

    def init_task_for_stages(self):
        for stage in self.stage_group.stages:
            self.stage_group.set_task_for_stage(stage.name, self.task)

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
        self.stage_group._get_stage_with_name(stage_name).start_constraint(
            constraint_name)

    def stop_constraint(self, stage_name, constraint_name):
        self.stage_group._get_stage_with_name(
            stage_name).stop_constraint(constraint_name)

    def _start(self, stage_name=""):
        self.stage_group.start(stage_name)

    def start(self, stage_name=""):
        self.thread_ref = threading.Thread(
            target=self._start, args=[stage_name])
        self.thread_ref.start()

    def start_stage(self, stage_name):
        self.stage_group.start(stage_name)

    def abort(self):
        self.stage_group.stop_all()

    def stop_stage(self, stage_name):
        self.stage_group.stop_stage(stage_name)

    def pause_stage(self):
        self.current_stage.freeze()

    def get_next_constraint_or_stage(self, stage_name, constraint_name):
        all_stages = self.stage_group.stages

        stage_position = self._get_stage_position(stage_name)

        initial_stage = all_stages[stage_position-1]
        for i in range(stage_position, len(all_stages)+1):
            print(i)
            if initial_stage != None:
                constraints = initial_stage.constraints
                for constraint in constraints:
                    if initial_stage.name == stage_name and constraint.name != constraint_name and constraint.get_status() != ConstraintStatus.COMPLETE:
                        return {"stage_name": initial_stage.name, "constraint_name": constraint.name}
                    elif initial_stage.name != stage_name and constraint.get_status() != ConstraintStatus.COMPLETE:
                        return {"stage_name": initial_stage.name, "constraint_name": constraint.name}

                initial_stage = None

            stage_ = all_stages[i-1]
            constraints = stage_.constraints

            for constraint in constraints:
                print(stage_.name, constraint.name)
                if stage_.name == stage_name and constraint.name != constraint_name and constraint.get_status() != ConstraintStatus.COMPLETE:
                    return {"stage_name": stage_.name, "constraint_name": constraint.name}
                elif stage_.name != stage_name and constraint.get_status() != ConstraintStatus.COMPLETE:
                    return {"stage_name": stage_.name, "constraint_name": constraint.name}
        return {"stage_name": None, "constraint_name": None}

        # # Check if the constraint [constraint_name] is the last constraint in the stage
        # if constraints[len(constraints)-1].name == constraint_name:
        #     # The stage [stage_name] is the last in the StageGroup
        #     if stage_position == len(all_stages):
        #         return {"stage_name": None, "constraint_name": None}
        #     else:
        #         print(stage_position)
        #         return {"stage_name": all_stages[stage_position].name, "constraint_name": self._get_first_constraint_in_stage(all_stages[stage_position].name).name}
        # else:
        #     constraint_position = self._get_constraint_position(
        #         constraint_name, stage_name)
        #     if constraint_position == None:
        #         return {"stage_name": None, "constraint_name": None}

        #     return {"stage_name": stage_name, "constraint_name": self.get_stage(stage_name).constraints[constraint_position].name}

    def _get_stage_position(self, stage_name):
        all_stages = self.stage_group.stages
        for i in range(len(all_stages)):
            if all_stages[i].name == stage_name:
                return i+1

    def _get_constraint_position(self, constraint_name, stage_name):
        stage = self.get_stage(stage_name)
        for i in range(len(stage.constraints)):
            if stage.constraints[i].name == constraint_name:
                return i+1

    def _get_first_constraint_in_stage(self, stage_name):
        stage = self.get_stage(stage_name)
        return stage.constraints[0]

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
        for stage in self.stage_group.stages:
            print(f"STAGE name: {stage.name}")
            for cnstrt in stage.constraints:
                print(f"\t>>CONSTRAINT name: {cnstrt.name}")
            print()
