# Values are not needed
# k_threshold = 3
# n_threshold = 8


# Private polynomial
def p(x):
    return 3 + 5*x + 10*(x**2) + 11*(x**3)


# Private data points, probably not needed
# data = [p(1), 161, 568, 1565, 3578, 7153, 12956, 21773]

# Received data points f(1), index = participant index
received_data = [p(1), 45, 39, 41, 55, 45, 41]

# Received data points f(n), index = participant index
interpolation_points = [sum(received_data), 3313, 12939, 21430]

# Each x represent the index of each participant that's part of K, order corresponding to their submitted data
# Make sure to include 1, since we are always participating as 1
x_vals = [1, 3, 5, 6]
# For the sake of clarity
y_vals = interpolation_points


# Some Lagrange interpolation
def lagrange_interpolation(x, i, x_vals):
    y = 1.0
    for j in range(len(x_vals)):
        if not i == j:
            y *= (x-x_vals[j]) / (x_vals[i] - x_vals[j])
    return y


def interpolation(x, x_vals, y_vals):
    polynomial = [lagrange_interpolation(x, i, x_vals) for i in range(len(x_vals))]
    y = sum(x_i*y_i for x_i, y_i in zip(y_vals, polynomial))
    return y


# Just some printing
print("-"*23)
deactivation_code = interpolation(0, x_vals, y_vals)
print("Deactivation Code: " + str(round(deactivation_code)))
print("-"*23)
