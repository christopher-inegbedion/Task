from enum import Enum


class ModeOfExecution(Enum):
    """This describes how the task will be provided to the customer"""

    # The task will be provided to the customer by means of delivery
    DELIVERY = 0

    # The customer will have to meet with the service provider
    MEET_UP_SP = 1

    # The service provider will have to meet with the customer
    MEET_UP_CSTMR = 2

    # The customer and service provider do not meet up together
    ONLINE = 3
