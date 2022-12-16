"""
Defines the cost functions. Can be extended.

"""


def linear_squared_cost(length: float, grade: float):
    if grade > 0:
        return length + (100 * grade) ** 2
    else:
        return length + grade


cost_functions_map = {
    "linear_squared_cost": linear_squared_cost
}
