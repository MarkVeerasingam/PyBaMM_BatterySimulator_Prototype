import pybamm

def simulate_battery():
    try:
        # Create a PyBaMM model, i'll use DFN for simplicity
        model = pybamm.lithium_ion.DFN()

        # Parameter sets are premade parameters based off recognised experiemtns
        # https://docs.pybamm.org/en/stable/source/api/parameters/parameter_sets.html
        custom_parameters = pybamm.ParameterValues("Chen2020")
        # custom_parameters = model.default_parameter_values 

        # change the current function to be an input parameter.
        custom_parameters["Lower voltage cut-off [V]"] = "[input]"
        custom_parameters["Upper voltage cut-off [V]"] = "[input]"

        # There is a high tolerence to battery simulations, this may lead to
        # "Error: Events ['Maximum voltage [V]'] are non-positive at initial conditions".
        # Source Code: https://tinyurl.com/39kc5jm6
        # Solution 1): custom_parameters = model.default_parameter_values, however poor solving
        # Solution 2): exception handelling
        custom_parameters.update({
            # Keep it relative to 2.5 -> 4.2 V simulations, SolverError is triggered if not
            "Lower voltage cut-off [V]": 2.5, 
            "Upper voltage cut-off [V]": 4.2, 
        }) 

        # Create and solve the PyBaMM simulation
        sim = pybamm.Simulation(model, parameter_values=custom_parameters)
            
        sim.solve([0, 3700]) 

        # Extract a simple result (e.g., voltage) for demonstration purposes
        # Source Code: https://tinyurl.com/2s3c7zke
        voltage = sim.solution['Terminal voltage [V]'].entries.tolist()

        # Print or return the simulation results
        print("Simulation Results:")
        print("Voltage:", voltage)

    except pybamm.SolverError as e:
        print(f"Solver error: {str(e)}")
        print("Voltage cut-off values should be relative to 2.5V and 4.2V")
    except Exception as e:
        print("Error:", str(e))

# Run the simulation function
simulate_battery()
