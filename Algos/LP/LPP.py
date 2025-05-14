import numpy as np

def simplex(c, A, b):
    """
    Solves: Maximize cᵀx subject to Ax <= b, x >= 0
    Args:
        c: list of coefficients in objective function (maximize cᵀx)
        A: list of constraint coefficient rows
        b: list of RHS constants

    Returns:
        (optimal_value, variable_values) or (None, None) if infeasible/unbounded
    """

    A = np.array(A, dtype=float)
    b = np.array(b, dtype=float)
    c = np.array(c, dtype=float)

    num_vars = len(c)
    num_constraints = len(b)

    # Add slack variables
    slack_identity = np.eye(num_constraints)
    tableau = np.hstack([A, slack_identity, b.reshape(-1, 1)])

    # Objective row (negated c, zero slack, RHS=0)
    obj_row = np.hstack([-c, np.zeros(num_constraints + 1)])
    tableau = np.vstack([tableau, obj_row])

    basis = list(range(num_vars, num_vars + num_constraints))

    while True:
        # Step 1: Check for optimality (if no negative coefficient in objective row)
        obj_coeffs = tableau[-1, :-1]
        if np.all(obj_coeffs >= 0):
            break  # Optimal

        # Step 2: Choose entering variable (most negative coefficient)
        entering = np.argmin(obj_coeffs)

        # Step 3: Check for unboundedness
        col = tableau[:-1, entering]
        if np.all(col <= 0):
            return None, None  # Unbounded

        # Step 4: Choose leaving variable (minimum ratio test)
        ratios = np.divide(tableau[:-1, -1], col, where=col > 0)
        ratios[col <= 0] = np.inf
        leaving = np.argmin(ratios)

        # Step 5: Pivot
        pivot_element = tableau[leaving, entering]
        tableau[leaving, :] /= pivot_element

        for i in range(len(tableau)):
            if i != leaving:
                tableau[i, :] -= tableau[i, entering] * tableau[leaving, :]

        basis[leaving] = entering

    # Extract solution
    x = np.zeros(num_vars)
    for i, var_index in enumerate(basis):
        if var_index < num_vars:
            x[var_index] = tableau[i, -1]

    optimal_value = tableau[-1, -1]
    return optimal_value, x
