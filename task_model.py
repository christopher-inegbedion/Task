from constraints.models.model_parent import *
from main.product_task import ProductTask


class TaskModel(Model):
    def __init__(self) -> None:
        self.name = "Task"
        self.model_family = ModelFamily.CONSTRAINT
        self.input_type = InputType.TASK
        self.input_mode = ConstraintInputMode.PRE_DEF
        self.input_count = 0
        self.output_type = InputType.BOOL

        super().__init__(self.name, self.model_family, self.input_type,
                         self.input_mode, self.input_count, self.output_type)

    def run(self, inputs: list):
        super().run(inputs)
        task: ProductTask = self.constraint.task_instance

        task.name = "new name"

        self._complete(False)

    def _complete(self, data, aborted=False):
        super()._complete(data)
