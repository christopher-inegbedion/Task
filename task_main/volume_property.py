from task_main.task_property import TaskProperty


class VolumeProperty(TaskProperty):
    def __init__(self) -> None:
        super().__init__("Volume", ["cm3", "m3"])
