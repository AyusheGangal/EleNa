def linear_squared_cost(length, grade):
    if grade > 0:
        return length + (100*grade)**2
    else:
        return length + grade


cost_functions_map = {
    "linear_squared_cost": linear_squared_cost
}
