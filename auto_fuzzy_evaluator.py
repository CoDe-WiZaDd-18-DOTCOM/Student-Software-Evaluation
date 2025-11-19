from metrics_extractor import extract_java_metrics, compute_fuzzy_inputs
from fuzzy_evaluator import system_ctrl
from skfuzzy import control as ctrl

project_path = r"C:\Users\jaswa\Desktop\carpooling"

metrics = extract_java_metrics(project_path)

print("\n========= EXTRACTED METRICS =========")
print("LOC:", metrics.loc)
print("Classes:", metrics.num_classes)
print("Methods:", metrics.num_methods)
print("Inheritance Depth:", metrics.inheritance_depth)
print("Estimated Cyclomatic Complexity:", metrics.total_cc)
print("Overrides:", metrics.overrides)

clean, func, inh = compute_fuzzy_inputs(metrics)

print("\n========= FUZZY INPUTS =========")
print("Clean Code:", clean)
print("Functionality:", func)
print("Inheritance:", inh)

sim = ctrl.ControlSystemSimulation(system_ctrl)
sim.input['clean_code'] = clean
sim.input['functionality'] = func
sim.input['inheritance'] = inh
sim.compute()

print("\n========= FINAL PROJECT SUCCESS =========")
print("Project Success Score:", round(sim.output['project_success'], 2))
