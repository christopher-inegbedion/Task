from main.task import Task
from task_pipeline.pipeline import Pipeline
from constraints.constraint_main.constraint import Constraint
from constraints.constraint_main.custom_constraint import CustomConstraint
from typing import List
import requests
from constraints.models.example_models.test_model import TestModel
from constraints.models.model_parent import Model
from stage.stage import Stage, StageGroup
from constraints.enums.constraint_input_mode import ConstraintInputMode
import time

addr = "http://192.168.1.129:8000/"

started = False
stages: List[Stage] = []
constraints = {
    "con1": CustomConstraint("con1", TestModel()),
    "con2": CustomConstraint("con2", TestModel()),
    "con3": CustomConstraint("con3", TestModel()),
}
stage_group: StageGroup = None
pipeline: Pipeline = None

models: List[Model] = {
    TestModel().name: TestModel()
}


def main():
    while True:
        action = input("\ncommand: ")

        if action == "exit":
            return False
        else:
            parse_action(action)


def perform_network_request(url, action):
    if action == "get":
        r = requests.get(url)
    elif action == "post":
        r = requests.post(url)

    if r.status_code == 200:
        response = r.json()
        return response

    return False


def parse_network_action(action):
    if action == "exit":
        return False
    elif action == "commands":
        command_addr = addr + f"commands/{action}"
        response = perform_network_request(command_addr, "get")

        print()
        for command in response["available_commands"]:
            print(command)


def parse_action(action):
    if action == "exit":
        return False
    else:
        if action == "commands":
            display_commands()
        elif action == "create stage":
            create_stage()
        elif action == "create constraint":
            create_constraint()
        elif action == "all constraints":
            view_all_constraints()
        elif action == "all stages":
            view_all_stages()
        elif action == "all models":
            view_all_models()
        elif action == "init stage group":
            init_stage_group()
        elif action == "init pipeline":
            init_pipeline()
        elif action == "run":
            run_pipeline()
        elif action == "run constraint":
            run_constraint()
        elif action == "abort":
            stop_pipeline()
        elif action == "stop stage":
            stop_stage()
        elif action == "stop constraint":
            stop_constraint()
        else:
            print(f"\ncommand '{action}' is not recognized\n")


def display_commands():
    print()
    print("'create stage' - Create a stage, with constraints")
    print("'create constraint' - Create a constraint with a model")
    print("'all constraint' - List all the constraints")
    print("'all stages' - List all the stages")
    print("'all models' - List all the models")
    print("'init stage group' - Initialise a stage group")
    print("'init pipeline' - Initialise a pipeline")
    print("'run' - Run a pipeline")
    print("'run constraint' - Run a constraint")
    print("'abort' - Stop a pipeline")
    print("'stop stage' - Stop a stage")
    print("'stop constraint' -  Stop a constraint")
    print("--------------")


def init_stage_group():
    global stage_group

    if len(stages) == 0:
        print("\nThere are no stages")
        print("run 'create stage' to create a stage\n")
    else:
        stage_group = StageGroup()
        for stage in stages:
            stage_group.add_stage(stage)

        print("\n[new] Stage group created with the following stages [new]")
        for stage in stage_group.stages:
            print(f"\t- {stage.name}")
        print("\nSuggested next command: 'init pipeline'")

    print("--------------\n")


def init_pipeline():
    global pipeline

    if stage_group == None:
        print("\nA stage group has not been created")
        print("run 'init stage group' to initialize a stage group\n")
    else:
        task = Task("", "")
        task.set_constraint_stage_config(stage_group)
        pipeline = Pipeline(task, stage_group)

        print("\n[new] Pipeline created [new]\n")
        print("Suggested next command: 'run'")
    print("--------------\n")


def stop_pipeline():
    if pipeline == None:
        print("\nA pipeline has not been created\n")
        print()
    else:
        pipeline.abort()


def stop_stage():
    if pipeline == None:
        print("\nA pipeline has not been created\n")
        print()
    else:
        stage_name = input(">Enter the stage to stop: \n")
        pipeline.stop_stage(stage_name)


def stop_constraint():
    if pipeline == None:
        print("\nA pipeline has not been created\n")
        print()
    else:
        stage_name = input(">Enter the stage's name: ")
        constraint_name = input(">Enter the constraint's name: \n")
        pipeline.stop_constraint(stage_name, constraint_name)


def run_pipeline():
    if pipeline == None:
        print("\nA pipeline has not been created")
        print("run 'init pipeline' to initialize a pipeline\n")
    else:
        print("--PIPELINE started--")
        print("\nSuggested next command: 'run constraint'\n")
        pipeline.start()
        time.sleep(0.1)
    print("--------------\n")


def run_constraint():
    if pipeline == None:
        print("\nA pipeline does not exist")
        print("run 'init pipeline' to initialize a pipeline\n")
    else:
        stage_name = input("input stage name: ")

        does_stage_exist = False
        for stage in stages:
            if stage.name == stage_name:
                does_stage_exist = True

        if does_stage_exist:
            constraint_name = input("input constraint name: ")

            if constraint_name in constraints:
                if constraints[constraint_name].model.input_mode == ConstraintInputMode.PRE_DEF or constraints[constraint_name].model.input_mode == ConstraintInputMode.MIXED_USER_PRE_DEF:
                    for i in range(constraints[constraint_name].model.input_count):
                        constraint_input = input(
                            f"Provide input {i} for constraint {constraint_name}: ")
                        constraints[constraint_name].add_input(
                            constraint_input)

                pipeline.start_constraint(stage_name, constraint_name)
            else:
                print(
                    f"\nConstraint '{constraint_name}' cannot be found.\n")
        else:
            print(f"\nStage '{stage_name}' does not exist")

    print("--------------\n")


def view_all_stages():
    if len(stages) > 0:
        for stage in stages:
            print(f"{stage.name}:")
            for constraint in stage.constraints:
                print(
                    f"\t- Constraint name: {constraint.name} [Model: {constraint.model.name}]")
    print("--------------\n")


def view_all_models():
    if len(models) > 0:
        for model in models:
            print(f"- {model}")
        print()
        print("--------------\n")
    else:
        print("[x]There are no models[x]")


def view_all_constraints():
    if len(constraints) > 0:
        for constraint in constraints:
            print(
                f"- Constraint name: {constraint} [Model: {constraints[constraint].name}]")
        print()
        print("--------------\n")
    else:
        print("There are no constraints")


def create_stage():
    if len(constraints) == 0:
        print("\nA constraint has not been created")
        print("run: 'create constraint' to create a constraint\n")
    else:
        name = input(">What is the stage name: ")

        print("These are the constratins available")
        for constraint in constraints:
            print(
                f"- {constraint} [Model: {constraints[constraint].model.name}]")

        new_stage = Stage(name)
        print()

        while True:
            constraint_name = input(
                ">Select the constraint to add to the stage: ")
            if constraint_name != "exit":
                if constraint_name in constraints:
                    selected_constraint: Constraint = constraints[constraint_name]
                    new_stage.add_constraint(selected_constraint)
                else:
                    print(
                        f"A constraint named '{constraint_name}' cannot be found.")
            else:
                print(
                    f"\n[new] Stage '{name}' created\n")
                break
        stages.append(new_stage)
        print("Suggested next command: 'init stage group'")
    print("--------------\n")


def create_constraint():
    print("\nThese are the models available")
    for model in models:
        print(f"- {model}")

    constraint_model = input(">What model should be used for the constraint: ")
    selected_model = select_model(constraint_model)

    model_name = input(">What is the name of the constraint: ")
    new_constraint = CustomConstraint(model_name, selected_model)

    constraints[model_name] = new_constraint

    print(
        f"[new] Constraint name: {new_constraint.name}, model: {new_constraint.model.name} [new]\n")
    print("Suggested next command: 'create stage'")
    print("--------------\n")
    return new_constraint


def select_model(model_name) -> Model:
    model = models[model_name]
    if model == None:
        return False
    else:
        return model


main()
