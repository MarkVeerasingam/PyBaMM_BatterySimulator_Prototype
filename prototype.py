import pybamm
import numpy as np

# Input time
hours = int(input("Please enter hours:"))
seconds = hours * 60 * 60
print(seconds, " Seconds")

def simulate_battery():
    try:
        # Create a PyBaMM model, i'll use DFN for simplicity
        model = pybamm.lithium_ion.DFN()
        custom_parameters = pybamm.ParameterValues("Chen2020")

        # set mesh with dict (all default)
        var_pts = {
        "x_n": 30,  # negative electrode
        "x_s": 30,  # separator
        "x_p": 30,  # positive electrode
        "r_n": 10,  # negative particle
        "r_p": 10,  # positive particle
        }

        # Create Solvers
        # load solvers
        safe_solver = pybamm.CasadiSolver(atol=1e-6, rtol=1e-6, mode="safe")
        fast_solver = pybamm.CasadiSolver(atol=1e-3, rtol=1e-3, mode="fast")

        # Parameter sets are premade parameters based off recognised experiemtns
        # https://docs.pybamm.org/en/stable/source/api/parameters/parameter_sets.html
        # custom_parameters = model.default_parameter_values 

        # There is a high tolerence to battery simulations, this may lead to
        # "Error: Events ['Maximum voltage [V]'] are non-positive at initial conditions".
        # Source Code: https://tinyurl.com/39kc5jm6
        # Solution 1): custom_parameters = model.default_parameter_values, however poor solving
        # Solution 2): exception handelling

        # Params should be, Voltage(min/max), current, Cell Capacity for now. 
        # String Experiments could be cool jupyer notebook example: https://tinyurl.com/kue58phd
        custom_parameters.update({ # all values below are default
            "Upper voltage cut-off [V]":    4.2, 
            "Lower voltage cut-off [V]":    2.5, 
            "Nominal cell capacity [A.h]":  8.5, # in Ah, typically recorded in mAh
            "Current function [A]":         4  # Make this non changeable for now 
        }) 
        # https://tinyurl.com/4zynbp7c Look at making a custom current func for current function [A]

        # Create and solve the PyBaMM simulation
        # sim = pybamm.Simulation(model, parameter_values=custom_parameters, solver=casadi_solver)
        safe_sim = pybamm.Simulation(model, parameter_values=custom_parameters, solver=safe_solver, var_pts=var_pts)
        fast_sim = pybamm.Simulation(model, parameter_values=custom_parameters, solver=fast_solver, var_pts=var_pts)

        t_eval = np.arange(0, 121, 1)

        solution = safe_sim.solve([0,seconds]) 
        # Look at simulating drive cycles t_eval, initial_soc, c rate, could be a cool feature for EV
        # solution = safe_sim.solve(t_eval=t_eval) prints no time value but has a cool changing current feature. this could be cool to look at later on for non "time based simulations"

        # Source Code: https://tinyurl.com/2s3c7zke
        time_s = solution['Time [s]'].entries
        voltage = solution['Battery voltage [V]'].entries
        current = solution['Current [A]'].entries
        dcap = solution['Discharge capacity [A.h]'].entries

        print("Time [s]\tVoltage\t\tCurrent\t\tDischarge Capacity")
        for t, v, i, dc in zip(time_s.data, voltage.data, current.data, dcap.data):
            print(f"{t:.2f}\t\t{v:.4f}\t\t{i:.4f}\t\t{dc:.4f}", flush=True)
        
    except pybamm.SolverError as e:
        print(f"Solver error: {str(e)}")
        print("Voltage cut-off values should be relative to 2.5V and 4.2V")
    except Exception as e:
        print("Error:", str(e))

# Run the simulation
simulate_battery()
