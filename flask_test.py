import pybamm
from flask import Flask, request, jsonify

app = Flask(__name__)

def simulate_battery(params, hours):
    try:
        # Your existing code for battery simulation here...
        model = pybamm.lithium_ion.DFN()
        safe_solver = pybamm.CasadiSolver(atol=1e-6, rtol=1e-6, mode="safe")

        custom_parameters = pybamm.ParameterValues("Chen2020")
        custom_parameters.update(params)

        safe_sim = pybamm.Simulation(model, parameter_values=custom_parameters, solver=safe_solver)
        
        seconds = hours * 60 * 60
        solution = safe_sim.solve([0, seconds])

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
        data = request.get_json()

        # Update parameters based on data received from Java
        hours = data.get('Time [hr]', 1)
        custom_parameters = {
            "Upper voltage cut-off [V]": data.get("Upper Voltage Cut-Off", 4.2),
            "Lower voltage cut-off [V]": data.get("Lower Voltage Cut-Off", 2.5),
            "Nominal cell capacity [A.h]": data.get("Nominal Cell Capacity [aH]", 8.6),
            "Current function [A]": 2 # dont change
        }

        # Call the battery simulation function
        simulation = simulate_battery(custom_parameters, hours)

        return jsonify(simulation)

    except Exception as e:
        return jsonify(error=str(e))

if __name__ == '__main__':
    app.run(debug=True, port=8084)
