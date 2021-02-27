from enum import Enum


class TaskType(Enum):
    """There are 2 types of tasks.

    PRODUCT: A task that provides a customer with a physical product
    SERVICE: A task that provides a customer with a service
    """
    PRODUCT = 0
    SERVICE = 1
