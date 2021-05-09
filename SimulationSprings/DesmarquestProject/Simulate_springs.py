import numpy as np
import csv
import pandas as pd
import matplotlib.pyplot as plt
from integration_methods import EulerScheme, ImplicitMidpoint

class SpringsSystem:
    def __init__(self, n=5, x=None, y=None, m=None, k=None, L=None, b=None, seed=None):
        """
        Initialize the System of n bodies connected by springs.
        Arguments:
            n (int) : Number of bodies,
            x (array type) : Array of initial position. Be randomly Initialized by default.
            y (array type) : Array of initial velocity. Be randomly Initialized by default.
            m (array type) : Masses of the bodies
            k (array type) : Resistence of Springs
            L (array type) : Length of Springs
            b (array type) : Friction of bodies
            seed (int) : Set a seed if we want to replicate the explirence

        """
        self.n = n
        # Parameter values
        # Masses:
        if m is None:
            m = [1.] * n
        # Spring constants
        if k is None:
            k = [2.] * (n+1)
        # Natural lengths
        if L is None:
            L = [1.] * (n+1)
        # Friction coefficients
        if b is None:
            b = [0.] * n
        # Pack up the parameters and initial conditions:
        self.p = {'m' : m,
            'k': k,
            'L': L,
            'b' : b}

        if seed is not None:
            np.random.seed(seed)

        # Initial conditions
        # x are the initial displacements
        if x is None:
            x = []
            for i in range(n+1):
                x.append(i + np.random.uniform(-0.5, 0.5))
        if y is None:
            y = []
            for i in range(n+1):
                y.append( np.random.uniform(-0.5, 0.5))
        names = [] # column names for the data
        w0 = [] # Initial conditions
        for i in range(n):
            w0.append(x[i])
            w0.append(y[i])
            names.append('x'+str(i))
            names.append('y'+str(i))
        self.w0 = w0
        self.names = names

    def vectorfield(self, w, t, p):
        """
        Defines the differential equations for the coupled spring-mass system.

        Arguments:
            w (list):  vector of the state variables:
                      w = [x1,y1,x2,y2, ..., xn, yn]
            t (float):  time, not used but necessary for using odeint.
            p (dict):  Dictionary of the parameters: keys are:
                                - 'm' : masses,
                                - 'k' : resistent coefficients
                                - 'L' : length of each spring
                                - 'b' : friction coefficients
        """
        x = [] # Position
        y = [] # Velocity
        for i in range(int(len(w)/2)):
            x.append(w[2*i])
            y.append(w[2*i+1])

        m = p['m']
        k = p['k']
        L = p['L']
        b = p['b']

        # The spring is attached to 0 and to this end_point/
        end_point = sum(L)
        n = len(x)

        # f = (x1', y1', ..., xn', yn')

        f = [y[0],
            (-b[0] * y[0] - k[0] * (x[0] - L[0]) + k[1] * (x[1] - x[0] - L[1])) / m[0]]
        for i in range(1, n-1):
            f += [y[i], (-b[i] * y[i] - k[i] * (x[i] - x[i-1] - L[i]) + k[i+1] * (x[i+1] - x[i] - L[i+1])) / m[i]]
        f += [y[n-1],
             (-b[n-1] * y[n-1] + k[n] * (end_point - x[n-1] - L[n]) - k[n-1] * (x[n-1] - x[n-2] - L[n-1])) / m[n-1]]
        return f

    def simulate(self, t=None, method=ImplicitMidpoint, stoptime=10.0, numpoints=250):
        """
        Simulate for the time t the system.
        Arguments:
            t (array) : array of timesteps
            method (method): Which method to use
            stoptime (flot) : stoptime (used if t is None)
            numpoints (int): Number of timesteps (used if t is None)
        Return:
            data (pd.DataFrame): Simulated data
        """
        if t is None:
            t = [stoptime * float(i) / (numpoints - 1) for i in range(numpoints)]
        # Call the ODE solver.
        wsol = method(self.vectorfield, self.w0, t, self.p, constraint=self.constraint)
        data = pd.DataFrame(wsol, columns=self.names)
        return data

    def save_data(self, data, title='Springs.csv'):
        """
        Save data in a csv file.
        Arguments:
            data (pd.DataFrame) : Simulated DataFrame
            title (str): Title
        """
        with open(title, 'w', newline='') as csvfile:
            # Print & save the solution.
            for t1, w1 in zip(t, data):

                spamwriter = csv.writer(csvfile, delimiter=',',
                                        quotechar='|', quoting=csv.QUOTE_MINIMAL)
                spamwriter.writerow(w1)

    def constraint(self, row, L, eps=1e-3):
        """
        Constraints for the system: the bodies can not surpass 0 and L, and the
        bodies can not intersect and pass each other.
        Arguments:
            row (array type): The array of position and velocity of the bodies at
                a certain time.
            L (float): Constraint above (cannot surpass it)
            eps (float): For accuracy
        Return:
        The modified row
        """
        for i in range(int(len(row)/2)):
            if row[2*i] < eps:
                row[2*i] = eps
                row[2*i + 1] = - row[2*i + 1]
            if row[2*i] > L:
                row[2*i] -= eps
                row[2*i + 1] = - row[2*i + 1]
        for i in range(1, int(len(row)/2)):
            if (row[2*i] - row[2*(i-1)]) < eps:
                diff = (row[2*i] - row[2*(i-1)])/2
                temp = row[2*i]
                row[2*i] = row[2*(i-1)]
                row[2*(i-1)] = row[2*i]
                row[2*i + 1] = - row[2*i + 1]
        return row


    def plot_position(self, data=None, title='Mass Displacements for the\nCoupled Spring-Mass System', figsize=(6, 4.5)):
        """
        Plot the position of the bodies for a simulation.
        Arguments:
            data (pd.DataFrame or None): Simulated data. Default : simulate it.
            title (str): title of the plot
            figsize (tuple)
        """
        plt.figure(1, figsize=figsize)
        plt.xlabel('t')
        plt.grid(True)
        lw = 1
        if data is None:
            data = self.simulate()
        for col in data:
            if col[0] == 'x':
                plt.plot(data[col], linewidth=lw, label=col)
        plt.legend()
        plt.title(title)

    def plot_velocity(self, data=None, title='Mass Velocity for the\nCoupled Spring-Mass System', figsize=(6, 4.5)):
        """
        Plot the velocity of the bodies for a simulation.
        Arguments:
            data (pd.DataFrame or None): Simulated data. Default : simulate it.
            title (str): title of the plot
            figsize (tuple)
        """
        plt.figure(1, figsize=figsize)
        plt.xlabel('t')
        plt.grid(True)
        lw = 1
        if data is None:
            data = self.simulate()
        for col in data:
            if col[0] == 'y':
                plt.plot(data[col], linewidth=lw, label=col)
        plt.legend()
        plt.title(title)
