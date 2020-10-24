# test model creation in Python
import unittest
import cosmo_python as cosmo

import numpy as np
from scipy import sparse


P = sparse.csc_matrix([[4., 1], [1, 2]])
q = np.array([1., 1])
A = sparse.csc_matrix([[1., 1], [1, 0], [0, 1]])
l = np.array([1., 0, 0])
u = np.array([1, 0.7, 0.7])

Aa = sparse.vstack((A, -A), format = 'csc')
# ba = np.vstack((u, -l))
ba = np.array([1, 0.7, 0.7, -1, 0, 0])
cone = {"l" : 6 }


model = cosmo.Model()

model.setup(P, q, Aa, ba, cone, verbose = True, kkt_solver = "CholmodKKTSolver")
x = np.array([1., 0])
model.warm_start(x)
model.optimize()

x = model.get_x()
obj_val = model.get_objective_value()

print("Solved with obj: ", obj_val)
