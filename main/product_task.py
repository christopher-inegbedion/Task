from enums.task_type import TaskType
from main.task import Task


class ProductTask(Task):
    """A product task. This is for service providers who want to deliver a product to their customers"""

    def __init__(self, name, description):
        super.__init__(name, description)
        # A product task type
        self.task_type = TaskType.PRODUCT

        # Being that this is a product task type an inventory system is needed to manage the products
        self.inventory = None
