# PyBaMM_BatterySimulator_Prototype
## About
- PyBaMM (Python Battery Mathematical Model) is developed by Ionworks, The Faraday Institution and NumFocus.
  Partnering with universitys like Oxford and University of Michigan, both recognised leaders in Battery Technology R&D.
              
  PyBaMM is an electrochemical simulation framework that offers a platform for formulating and solving differential equations related to batteries. 
  It includes a library of battery models, parameters, and tools for simulating battery experiments and visualizing results.
              
  https://pybamm.org/

## Notes:  
- All simulations are performed at ~25°.
- ALl simulations are solved on a "safe mode" with CasadiSolver https://tinyurl.com/mrxm9b96
- Changing "Current Function [A]" to a non reflective value of a batteries input
  can result in poor integration when solving and can produce errors and incomplete models.

## Todo:   
- Add validation and mandatory inputs (vmin/vmax, capacity and time) current can be changed but cautioun it to break ODE Solving tolerence
- Develop a flask runner client (maybe swagger codegen)
- Make lithium_ion models be custom param i.e. DFN, SPM, SPMe could be Model 1, Model 2... 
- Work with higher degree temperatures when simulating
- Make a parameter function | it should just handle parameter.update() and pass out an arg to simulate_battery()
