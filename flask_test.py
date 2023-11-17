import pybamm
from flask import Flask, request, jsonify

app = Flask(__name__)

# From protoype
def simulate_battery():
    try:
        # Gnereate battery model, solver and params
        model = pybamm.lithium_ion.DFN()
        safe_solver = pybamm.CasadiSolver(atol=1e-6, rtol=1e-6, mode="safe")
        custom_parameters = pybamm.ParameterValues("Chen2020")

    except pybamm.SolverError as e:
        return {"error": f"Solver error: {str(e)}"}
        print("Voltage cut-off values should be relative to 2.5V and 4.2V")
    except Exception as e:
        return {"error": f"Error: {str(e)}"}

if __name__ == '__main__':
    app.run(debug=True, port=8084)
