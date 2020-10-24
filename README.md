# Python interface for COSMO.jl

This is a thin Python-wrapper around the Julia package [COSMO.jl](https://github.com/oxfordcontrol/COSMO.jl). COSMO is a general purpose solver for convex conic optimisation problems of the form:
<p align="center">
<img src="https://github.com/migarstka/COSMO_assets/blob/master/cosmo_format.png" width=220px>
</p>


with decision variables `x ϵ R^n`, `s ϵ R^m` and data matrices `P=P'>=0`, `q ϵ R^n`, `A ϵ R^(m×n)`, and `b ϵ R^m`. 


<p align="center">
  <a href="#example">Example</a> •
  <a href="#installation">Installation</a> •
  <a href="https://oxfordcontrol.github.io/COSMO.jl/stable/">Documentation</a> •
  <a href="https://github.com/oxfordcontrol/COSMO.jl">Main repository</a> 
</p>

## Installation
The wrapper makes a call to Julia via the pyjulia interface. To set this up:

**On the Julia side:**

1. Install the *Julia* programming language (`v1.5+` recommended) [[Julia Download page]](https://julialang.org/downloads/)

2. Open the Julia REPL and install the Julia package `COSMO.jl`: `(type ]): pkg> add COSMO` (at least `v0.7.6+`)

**On the Python side:**

3. Install `pyjulia` the interface that lets you call Julia code from Python: `python3 -m pip install julia` 

4. In Python run `import julia` followed by `julia.install()` to finish the `pyjulia` setup.

5. Install this package: `git clone git@github.com:oxfordcontrol/cosmo-python.git` (for now, later via pip / conda)


## Example
This is a quick example to show the syntax of the wrapper. You can also use the example to verify that the steps in **Installation** were succesful. We want to solve the following quadratic program:
```
minimize 1/2 x' [4, 1; 1 2] x + [1;1]' x
s.t.     A x == b 
         x >= 0
```
```python
import cosmopy as cosmo
import numpy as np
from scipy import sparse

# define the problem
P = sparse.csc_matrix([[4., 1], [1, 2]])
q = np.array([1., 1])
A = sparse.csc_matrix([[1., 1], [1, 0], [0, 1], [-1., -1], [-1, 0], [0, -1]])
b = np.array([1, 0.7, 0.7, -1, 0, 0])
cone = {"l" : 6 }

# create a solver model
model = cosmo.Model()

# setup the model with the problem data and some optional solver settings
model.setup(P = P, q = q, A = A, b = b, cone = cone, verbose = True, eps_abs = 1e-5, max_iter = 4000)

# optional: warm starting of x
x = np.array([1., 0])
model.warm_start(x = x)

# solve the problem
model.optimize()

# query solution info
obj_val = model.get_objective_value() # optimal objective vale
status = model.get_status() # solution status
iter = model.get_iter() # number of iterations until convergence
times = model.get_times() # a dictionary of timings 
x_opt = model.get_x() # query the optimal primal variable x_opt

print("Solved with objective value: ", obj_val, " in", times["solver_time"], "s.")
```
More examples can be found in [/examples](https://github.com/oxfordcontrol/cosmo-python/tree/master/examples)

## Documentation
These notes only refer to the usage of this wrapper. For a general overview take a look at the [Documentation](https://oxfordcontrol.github.io/COSMO.jl/stable/) of the Julia package.

A `Model` is a thin Python class that wraps a `COSMO.Model` type in Julia.
```python
import cosmopy as cosmo
model = cosmo.Model()
```
The function `setup` copies the problem data and settings to the model:
```python
def setup(P = None, q = None, A = None, b = None, cone = None, settings**)
```
The input to the function should be:
- `P`, `A`: `scipy.sparse.csc_matrix`. Note that for PSD constraints the off-diagonals of A have to be scaled appropriately (see details below).
- `q`, `b`: `np.array`
- `cone`: A dictionary that holds the dimensions of the conic constraints in the following order and corresponding to the rows in `A` (following SCS convention):


| key        | value           | constraint  | corresponds to |
| ------------- |:-------------:| -----:|------ |
| "f"      | number of equality constraints | zero cone |  `COSMO.ZeroSet` |
| "l"      | number of inequality constraints |  nonegative orthant | `COSMO.Nonnegatives` |
| "q" | list of SOC sizes  | second order cone(s) | `COSMO.SecondOrderCone` |
| "s" | list of SDP sizes  | PSD cone | `COSMO.PsdConeTriangle` |
| "ep" | number of primal exp cones  | exp cone (p) | `COSMO.ExponentialCone` |
| "ed" | number of dual exp cones  | exp cone (d) | `COSMO.DualExponentialCone` |
| "p" | list of power cone parameters (neg value for dual)  | PSD cone | `COSMO.PowerCone` |

So if you want to create a problem with 2 equality constraints, 3 inequality constraints, 2 SOC-constraints of dim 3, 1 PSD-constraint for a 3x3 matrix, 1 PSD-constraint for a 4x4 matrix, 2 primal exponential cones, 1 dual exponential cone, 2 primal power cones with exponent `0.3` and `0.4` and one dual exponential cone with exponent `0.5`, define `cone` as follows:
```python
cone = {"f" : 2, "l" : 3, "q" : [3, 3], "s" : [6, 10], "ep" : 2, "ed": 1, "p" : [0.3, 0.4, -0.5] }
```

The solver settings can be passed into `setup` as key-value arguments. A list of all solver settings can be found [here](https://oxfordcontrol.github.io/COSMO.jl/stable/getting_started/#Settings-1). The only difference is that settings related to the `kkt_solver` and to the `merge_strategy` keys have to be passed as strings. So if you want to configure `COSMO` to use max 5000 iterations, the QDLDL solver for the linear system and the ParentChild clique merging strategy pass the following:
```python
model.setup(..., max_iter = 5000, kkt_solver = "QDLDLKKTSolver", merge_strategy = "ParentChildMerge")
```

Before we attempt to solve the problem, we can provide COSMO with initial guesses for the primal `x` and dual variables `y`:
```python
def warm_start(self, x=None, y=None):
```

The `model.optimize()` function calls the Julia equivalent: `COSMO.optimize!(model)` and solves the problem.

The following functions can be used to query the results:
```python
def get_objective_value(self): #optimal objective value

def get_x(self): #optimal primal variable

def get_y(self): #optimal dual variable

def get_s(self): #optimal slack variable

def get_status(self): #solution status

def get_iter(self): #number of iterations of algoritm

def get_times(self): #dict of timing information
```

## Licence
This project is licensed under the Apache License - see the [LICENSE.md](LICENSE.md) file for details.
