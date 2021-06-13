from time import sleep
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
from constraints.models.example_models.internet_model import InternetModel


# constraint1 = CustomConstraint("test1", TestModel())
# constraint1.add_input(4)
# constraint2 = CustomConstraint("test2", TestModel())

# constraint3 = CustomConstraint("test3", TestModel())
# constraint3.add_input(4)

# time_constraint = CustomConstraint(
#     "time", PauseModel()
# )

# task_constraint = CustomConstraint("task constraint", TaskModel())

# combined_constraint = CustomConstraint(
#     "combined constraint", TestCombinedConstraintModel())
# combined_constraint.add_input(constraint1)
# combined_constraint.add_input(constraint2)

# stage = Stage("PENDING")
# # stage.add_constraint(time_constraint)
# stage.add_constraint(combined_constraint)

# stage_group = StageGroup()
# stage_group.add_stage(stage)
# # stage_group.add_stage(stage2)


# shoes_entry = Entry()
# shoes_entry.add_entry("name", "Nike")
# shoes_entry.add_entry("size", 9)
# shoes_entry.add_entry("color", "blue")

# my_inventory = Inventory()
# my_inventory.add_entry(shoes_entry)

# new_task = ProductTask("Test task", "Create task")
# new_task.set_inventory(my_inventory)
# new_task.set_constraint_stage_config(stage_group)
# new_task.set_mode_of_execution(ModeOfExecution.ONLINE)
# new_task.set_price_constraint(combined_constraint)

# pipeline = Pipeline(new_task, new_task.constraint_stage_config, False)
# new_task.add_constraint_to_stage(constraint3, "PENDING")

# # pipeline.log()


# # pipeline.add_input_to_constraint("time", "PENDING", 33)


# def react(pipe, args):
#     print("-", pipe.current_stage.log.most_recent_update)
#     pass


# pipeline.on_constraint_complete(
#     react, "sd", "sdf")

# # pipeline.start()
# pipeline.start_stage("PENDING")
# pipeline.start_constraint("PENDING", "combined constraint")
# pipeline.start_constraint("PENDING", "test3")

def createCon1():
    return CustomConstraint("con", "desc", InternetModel(), debug=False)


def createCon2():
    return CustomConstraint("con2", "desc", InternetModel(), debug=False)


constraints = {
    "con": createCon1(),
    "con2": createCon2()
}


cons = createCon1()
cons1 = createCon2()
cons.add_input("EUR")
cons.add_input("USD")

cons1.add_input("NGN")
cons1.add_input("USD")

s = Stage('s')
s.add_constraint(cons)
s.add_constraint(cons1)

s2 = Stage('s2')
cons = createCon1()
cons.add_input("EUR")
cons.add_input("USD")
cons1 = constraints["con2"]
s2.add_constraint(cons)
s2.add_constraint(cons1)

s3 = Stage("s3")
cons = createCon1()
cons.add_input("EUR")
cons.add_input("USD")
cons1 = constraints["con2"]
s3.add_constraint(cons)
s3.add_constraint(cons1)

sg = StageGroup()
sg.add_stage(s)
sg.add_stage(s2)
sg.add_stage(s3)
# sg.add_stage(s2)

# sg.start('s')


def update(pipe, args):
    print(pipe.current_stage.log.most_recent_update)
# s.start_constraint("con")
# s.start_constraint("con2")


task = Task("name", "desc")
task.set_constraint_stage_config(sg)

pipe = Pipeline(task, sg)
# pipe.start()
# pipe.on_update(update)
# pipe.start_constraint("s", "con")
# sleep(2)
# pipe.start_constraint("s2", "con")
# pipe.start_constraint("s2", "con2")

pipe.start()
pipe.start_constraint("s", "con2")
pipe.start_constraint("s", "con")
time.sleep(1)
pipe.start_constraint("s2", "con")
time.sleep(1)
print(pipe.get_next_constraint_or_stage("s2", "con"))
