from enum import Enum


class StageStatus(Enum):
    """This describes the stage the task is at"""

    # The task has not been selected by the customer
    NOT_ENGAGED = 0

    # The customer has showed intent to start the task. This does not necesarily mean the task has begun.
    PENDING = 1

    # The task has begun and is active
    ACTIVE = 2

    # The task is active but its main job has been completed
    COMPLETE = 3
