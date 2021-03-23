from flask import Flask, jsonify

app = Flask(__name__)


def parse_action(action):
    if action == "exit":
        return False
    else:
        if action == "commands":
            return display_commands()
        # elif action == "create stage":
        #     create_stage()
        # elif action == "create constraint":
        #     create_constraint()
        # elif action == "all constraints":
        #     view_all_constraints()
        # elif action == "all stages":
        #     view_all_stages()
        # elif action == "all models":
        #     view_all_models()
        # elif action == "init stage group":
        #     init_stage_group()
        # elif action == "init pipeline":
        #     init_pipeline()
        # elif action == "run":
        #     run_pipeline()
        # elif action == "run constraint":
        #     run_constraint()
        # elif action == "abort":
        #     stop_pipeline()
        # elif action == "stop stage":
        #     stop_stage()
        # elif action == "stop constraint":
        #     stop_constraint()
        else:
            return f"command '{action}' is not recognized"


def display_commands():
    available_commands = {
        "available_commands": [
            "create stage -> Create a stage, with constraints",
            "create constraint -> Create a constraint with a model",
            "all constraint -> List all the constraints",
            "all stages -> List all the stages",
            "all models -> List all the models",
            "init stage group -> Initialise a stage group",
            "init pipeline -> Initialise a pipeline",
            "run -> Run a pipeline",
            "run constraint -> Run a constraint",
            "abort -> Stop a pipeline",
            "stop stage -> Stop a stage",
            "stop constraint -> Stop a constraint",
        ]
    }
    return jsonify(available_commands)

# Core server part


@app.route("/")
def main():
    return 'constraints and stages server'


@app.route("/commands/<command>")
def command(command):
    return parse_action(command)
