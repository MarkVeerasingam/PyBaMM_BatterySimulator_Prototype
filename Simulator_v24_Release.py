import pybamm
import numpy as np

# input temperature
temp_input = int(input("Please enter Temp Min:"))
temp_min = temp_input 
temp_input = int(input("Please enter Temp Max:"))
temp_max = temp_input 

model = pybamm.lithium_ion.DFN()
parameter_values = pybamm.ParameterValues("Chen2020")

# create geometry
geometry = model.default_geometry

# load parameter values and process model and geometry
def ambient_temperature(y, z, t):
    return 273 + temp_min + t * temp_max / 3600 

param = model.default_parameter_values
param.update(
    {"Ambient temperature [K]": ambient_temperature}, check_already_exists=False
)
param.process_model(model)
param.process_geometry(geometry)

# create our dictionary
var_pts = {
    "x_n": 30,  # negative electrode
    "x_s": 30,  # separator
    "x_p": 30,  # positive electrode
    "r_n": 10,  # negative particle
    "r_p": 10,  # positive particle
}
mesh = pybamm.Mesh(geometry, model.default_submesh_types, var_pts)

# discretise model
disc = pybamm.Discretisation(mesh, model.default_spatial_methods)
disc.process_model(model)

# solve model
t_eval = np.linspace(0, 3600 / 2, 100)
solver = pybamm.CasadiSolver(mode="fast", atol=1e-6, rtol=1e-3)
solution = solver.solve(model, t_eval)

temperature = solution["X-averaged cell temperature [C]"].entries

#print
print("Min Temperature:", np.min(temperature), "C")
print("Max Temperature:", np.max(temperature), "C")

# plot
plot = pybamm.QuickPlot(
    solution, ["X-averaged cell temperature [C]", "Ambient temperature [C]"]
)
plot.dynamic_plot()