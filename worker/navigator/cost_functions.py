def linear_squared_cost(length, grade):
    return (length + 1000 * grade) ** 2


cost_functions_map = {
    "linear_squared_cost": linear_squared_cost
}
