from task_main.task_property import TaskProperty

class WeightProperty(TaskProperty):
    def __init__(self) -> None:
        super().__init__("Weight", ["kg", "lb"])
