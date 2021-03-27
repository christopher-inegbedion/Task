from task_model import TaskModel
from task_pipeline.pipeline import Pipeline
from task_main.task import *
from inventory_main.inventory import Inventory, Entry
from task_main.task import Task
from task_main.product_task import ProductTask
from constraints.constraint_main.custom_constraint import CustomConstraint
from constraints.models.example_models.test_model import TestModel
from constraints.models.example_models.pause_thread import PauseModel
from constraints.models.example_models.test_combined_constraint import TestCombinedConstraintModel
from stage.stage import Stage
from utils.update import Observer


constraint1 = CustomConstraint("test1", TestModel())
constraint1.add_input(4)
constraint2 = CustomConstraint("test2", TestModel())

constraint3 = CustomConstraint("test1", TestModel())
constraint3.add_input(4)

time_constraint = CustomConstraint(
    "time", PauseModel()
)

task_constraint = CustomConstraint("task constraint", TaskModel())

combined_constraint = CustomConstraint(
    "combined constraint", TestCombinedConstraintModel())
combined_constraint.add_input(constraint1)
combined_constraint.add_input(constraint2)

stage = Stage("PENDING")
stage.add_constraint(time_constraint)
stage.add_constraint(combined_constraint)

stage2 = Stage("ACTIVE")
# stage2.add_constraint(combined_constraint)

stage_group = StageGroup()
stage_group.add_stage(stage)
stage_group.add_stage(stage2)


shoes_entry = Entry()
shoes_entry.add_entry("name", "Nike")
shoes_entry.add_entry("size", 9)
shoes_entry.add_entry("color", "blue")

my_inventory = Inventory()
my_inventory.add_entry(shoes_entry)

new_task = ProductTask("Test task", "Create task")
new_task.set_inventory(my_inventory)
new_task.set_constraint_stage_config(stage_group)
new_task.set_mode_of_execution(ModeOfExecution.ONLINE)
new_task.set_price_constraint(combined_constraint)

pipeline = Pipeline(new_task, new_task.constraint_stage_config, True)
# pipeline.log()
pipeline.start()

pipeline.add_input_to_constraint("time", "PENDING", 33)


async def react(pipe, args):
    print(args[0], args[1])


pipeline.on_update(True, react, "hello", 121, 2, 3)

pipeline.start_constraint("PENDING", "time")
pipeline.start_constraint("PENDING", "combined constraint")
# pipeline.log()
# time.sleep(2)
# pipeline.stop_constraint("PENDING", "time constraint")
# pipeline.start_constraint("ACTIVE", "combined constraint")
