from numpy import e, arctan, cos, sin, ones
import pyswarms as ps


def cal_function_value(values: list, minima=True) -> list:
    """Calculate the function values for all the solutions in the swarm."""
    calculations = []
    for pair in values:
        x, y = pair
        if minima:
            calculations.append(function(x, y))
        else:
        # If we want to find the maxima for the function we change the sign of the return value
            calculations.append(-function(x, y))
    return calculations


def function(x: float, y: float) -> float:
    """Definition of the function"""
    return (e ** (-0.05 * (x ** 2 + y ** 2))) * ((arctan(x) - arctan(y)) + (e ** - (x ** 2 + y ** 2)) * (cos(x) ** 2 * sin(y)) ** 2)


def pso():
    """Create one optimizer for minima and one for maxima. Find them and print the result."""
    options = {'c1': 0.5, 'c2': 0.5, 'w': 0.9}
    bounds = (-5*ones(2), 5*ones(2))

    # Optimizer for minima
    optimizer = ps.single.GlobalBestPSO(n_particles=100, dimensions=2, options=options, bounds=bounds)
    minima, pos_minima = optimizer.optimize(cal_function_value, 1000, verbose=False)

    # Optimizer for maxima
    optimizer = ps.single.GlobalBestPSO(n_particles=100, dimensions=2, options=options, bounds=bounds)
    # The value that is stored in maxima variable is negative, since we changed its sign in the calculation
    maxima, pos_maxima = optimizer.optimize(cal_function_value, 1000, verbose=False, minima=False)

    print(f'Det lägsta värdet för funktionen är {minima}, och finns på kooridnaterna {pos_minima}')
    print(f'Det högsta värdet för funktionen är {-maxima}, och finns på koordinaterna {pos_maxima}')

pso()

# Det lägsta värdet för funktionen är -1.5697840913957708, och finns på kooridnaterna [-1.52257709  1.52256797]
# Det högsta värdet för funktionen är 1.569784174244423, och finns på koordinaterna [ 1.52255974 -1.52256887]