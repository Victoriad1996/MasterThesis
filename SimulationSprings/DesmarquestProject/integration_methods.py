import numpy as np

def EulerScheme(vectorfield, w0, t, p, constraint):
    """
    Solve a system of ordinary differential equations with the EulerScheme.
    Arguments:
        vectorfield (method): dy/dt = vectorfield(y, t, ...). Method that computes the derivative.
        w0 (array type): Initial conditions
        t (array type): Array of timesteps
        p (dict): parameters for the vectorfield
    Return:
        solution(array type): Approximated solution
    """
    solution = np.zeros((len(t), len(w0)))
    solution[0,:] = w0
    for i in range(1, solution.shape[0]):
        solution[i,:] = solution[i-1,:] + (t[i]-t[i-1])*np.array(vectorfield(solution[i-1,:], t[i], p))
        solution[i,:] = constraint(solution[i,:], sum(p['L']))
    return solution

def ImplicitEuler(G, y, max_iterations=2000, eps=1e-6):
    """
    Implicit Euler method for finding a fixed point of a certain function.
    Arguments:
        G (method) : function.
        y (float) : Initial value
        max_iterations (int)
        eps (float) : accuracy
    Return:
        y1 (float): The fiwed point we approximated.
    """
    y0 = y
    y1 = G(y0)
    i = 1

    while ((np.linalg.norm(y1 - y0) > eps) and (i < max_iterations)):
        y0 = y1
        y1 = G(y1)
        i += 1
    return y1

def ImplicitMidpoint(vectorfield, w0, t, p, constraint):
    """
    Implicit mid point method for approximation of an ODE.
    Arguments:
        vectorfield (method): The f funtion of the ode
        w0 (array like): Initial values
        p (dict): parameters of the vectorfield
        constraint (method): contraint method to which the bodies are subject to.
    """
    solution = np.zeros((len(t), len(w0)))
    solution[0,:] = w0
    for i in range(1, solution.shape[0]):
        def G(y):
            return solution[i-1,:] + (t[i] - t[i-1]) * np.array(vectorfield((1/2)*(solution[i-1,:] + y), t, p))
        solution[i,:] = ImplicitEuler(G, solution[i-1,:])
        solution[i,:] = constraint(solution[i,:], sum(p['L']))
    return solution
