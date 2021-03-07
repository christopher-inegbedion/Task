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

addr = "192.168.1.129:5000/"

started = False
stages: List[Stage] = []
constraints = {}
stage_group: StageGroup = None
pipeline: Pipeline = None

models: List[Model] = {
    TestModel().name: TestModel()
}


def main():
    while True:
        action = input("action: ")

        if action == "exit":
            return False
        else:
            parse_action(action)


def parse_action(action):
    if action == "exit":
        return False
    else:
        if action == "create stage":
            create_stage()
        elif action == "create constraint":
            create_constraint(action)
        elif action == "init stage group":
            init_stage_group()
        elif action == "all models":
            view_all_models()
        elif action == "all constraints":
            view_all_constraints()
        elif action == "all stages":
            view_all_stages()
        elif action == "init pipeline":
            init_pipeline()
        elif action == "run":
            run_pipeline()
        elif action == "run constraint":
            run_constraint()
        elif action == "stop pipeline":
            pass


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


def init_pipeline():
    global pipeline

    if stage_group == None:
        print("\nA stage group has not been created")
        print("run 'init stage group' to initialize a stage group\n")
    else:
        task = Task("", "")
        task.set_constraint_stage_config(stage_group)
        pipeline = Pipeline(task, stage_group)

        print("[new] Pipeline created [new]")


def run_pipeline():
    if pipeline == None:
        print("\nA pipeline has not been created")
        print("run 'init pipeline' to initialize a pipeline\n")
    else:
        pipeline.start()


def run_constraint():
    if pipeline == None:
        print("\nA pipeline does not exist")
        print("run 'init pipeline' to initialize a pipeline\n")
    else:
        stage_name = input("input stage name: ")
        constraint_name = input("input constraint name: ")

        if constraints[constraint_name].model.input_mode == ConstraintInputMode.PRE_DEF or constraints[constraint_name].model.input_mode == ConstraintInputMode.MIXED_USER_PRE_DEF:
            for i in range(constraints[constraint_name].model.input_count):
                constraint_input = input(
                    f"Provide input {i} for constraint {constraint_name}: ")
                constraints[constraint_name].add_input(int(constraint_input))

        pipeline.start_constraint(stage_name, constraint_name)


def view_all_stages():
    if len(stages) > 0:
        for stage in stages:
            print(f"{stage.name}:")
            for constraint in stage.constraints:
                print(
                    f"\t- Constraint name: {constraint.name} [Model: {constraint.model.name}]")


def view_all_models():
    if len(models) > 0:
        for model in models:
            print(f"- {model}")
        print()
    else:
        print("There are no models")


def view_all_constraints():
    if len(constraints) > 0:
        for constraint in constraints:
            print(
                f"- Constraint name: {constraint} [Model: {constraints[constraint].name}]")
        print()
    else:
        print("There are no constraints")


def create_stage():
    if len(constraints) == 0:
        print("\n[A constraint has not been created]")
        print("run: 'create constraint' to create a stage\n")
    else:
        name = input("What is the stage name: ")

        print("These are the constratins available")
        for constraint in constraints:
            print(
                f"- {constraint} [Model: {constraints[constraint].model.name}]")

        new_stage = Stage(name)
        constraint_name = input(
            "\nSelect the constraint to add to the stage: ")
        selected_constraint: Constraint = constraints[constraint_name]
        stages.append(new_stage)

        print(f"[new] Stage -> Constraint(s): {constraint_name} [new]")
        new_stage.add_constraint(selected_constraint)


def create_constraint(constraint_name):
    print("\nThese are the models available")
    for model in models:
        print(f"- {model}")

    constraint_model = input("What model should be used for the constraint: ")
    selected_model = select_model(constraint_model)

    model_name = input("\nWhat is the name of the constraint: ")
    new_constraint = CustomConstraint(model_name, selected_model)

    constraints[model_name] = new_constraint

    print(
        f"[new] Constraint name: {new_constraint.name}, model: {new_constraint.model.name} [new]\n")
    return new_constraint


def select_model(model_name) -> Model:
    model = models[model_name]
    if model == None:
        return False
    else:
        return model


main()
