import pybamm
from flask import Flask, request, jsonify

app = Flask(__name__)

def simulate_battery(params, hours):
    try:
        # Create a Lithium Ion battery model with DFN, may look at having different models in the near future 
        model = pybamm.lithium_ion.DFN()

        # Casadi safe solver may be best for the nature of wanting to generate data correctly rather than fast
        safe_solver = pybamm.CasadiSolver(atol=1e-6, rtol=1e-6, mode="safe") # perform step-and-check integration in global steps of size dt_max 

        # Using a premade parameter set based off a LGM50 lithium Ion Cell, "Chen2020" is the name of the parameter set
        custom_parameters = pybamm.ParameterValues("Chen2020")
        custom_parameters.update(params)

        safe_sim = pybamm.Simulation(model, parameter_values=custom_parameters, solver=safe_solver) 
        
        seconds = hours * 60 * 60 # Pybamm solves in secnods, having the user input hour would make more sense
        solution = safe_sim.solve([0, seconds]) # solve  simulation from 0 seconds -> x ammount of seconds

        time_s = solution['Time [s]'].entries
        voltage = solution['Battery voltage [V]'].entries
        current = solution['Current [A]'].entries
        dcap = solution['Discharge capacity [A.h]'].entries

        result = {
            "Time [s]": time_s.tolist(),
            "Voltage": voltage.tolist(),
            "Current": current.tolist(),
            "Discharge Capacity": dcap.tolist()
        }

        return result

    except pybamm.SolverError as e:
        return {"error": f"SolverError:\nVoltage cut-off values should be relative to 2.5V and 4.2V: {str(e)}"}
    except Exception as e:
        return {"error": f"Error: {str(e)}"}

@app.route('/simulate', methods=['POST'])
def simulate():
    try:
        data = request.get_json() # Get data from post request

        # Update parameters based on data received (for this case, Java)
        hours = data.get('Time [hr]', 1)
        custom_parameters = {
            "Upper voltage cut-off [V]": data.get("Upper Voltage Cut-Off", 4.2),
            "Lower voltage cut-off [V]": data.get("Lower Voltage Cut-Off", 2.5),
            "Nominal cell capacity [A.h]": data.get("Nominal Cell Capacity [aH]", 8.6),
            "Current function [A]": 2 # dont change, until I can find a way to calc a better C rate 
        }

        # Call the battery simulation function
        simulation = simulate_battery(custom_parameters, hours)

        return jsonify(simulation) # return as a json

    except Exception as e:
        return jsonify(error=str(e))

if __name__ == '__main__':
    app.run(debug=True, port=8084)
