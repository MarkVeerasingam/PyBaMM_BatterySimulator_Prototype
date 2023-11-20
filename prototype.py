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

        # Create Solvers
        # load solvers
        safe_solver = pybamm.CasadiSolver(atol=1e-6, rtol=1e-6, mode="safe")
        fast_solver = pybamm.CasadiSolver(atol=1e-3, rtol=1e-3, mode="fast")

        # Parameter sets are premade parameters based off recognised experiemtns
        # https://docs.pybamm.org/en/stable/source/api/parameters/parameter_sets.html
        custom_parameters = pybamm.ParameterValues("Chen2020")
        # custom_parameters = model.default_parameter_values 

        # There is a high tolerence to battery simulations, this may lead to
        # "Error: Events ['Maximum voltage [V]'] are non-positive at initial conditions".
        # Source Code: https://tinyurl.com/39kc5jm6
        # Solution 1): custom_parameters = model.default_parameter_values, however poor solving
        # Solution 2): exception handelling

        # Params should be, Voltage(min/max), current, Cell Capacity for now. 
        # String Experiments could be cool jupyer notebook example: https://tinyurl.com/kue58phd
        custom_parameters.update({ # all values below are default
            "Upper voltage cut-off [V]":    4, 
            "Lower voltage cut-off [V]":    2.9, 
            "Nominal cell capacity [A.h]":  6.6, # in Ah, typically recorded in mAh
            "Current function [A]":         2  # Make this non changeable for now
        }) 

        # Create and solve the PyBaMM simulation
        # sim = pybamm.Simulation(model, parameter_values=custom_parameters, solver=casadi_solver)
        safe_sim = pybamm.Simulation(model, parameter_values=custom_parameters, solver=safe_solver)
        fast_sim = pybamm.Simulation(model, parameter_values=custom_parameters, solver=fast_solver)

        solution = safe_sim.solve([0, seconds]) #this is one hour, todo: user input specified time for solve
        # Look at simulating drive cycles t_eval, initial_soc, c rate, could be a cool feature for EV

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
