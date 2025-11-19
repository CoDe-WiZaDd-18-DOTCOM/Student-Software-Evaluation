import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl
import matplotlib.pyplot as plt


# -----------------------------
# 1. Define Universes
# -----------------------------
x = np.arange(0, 101, 1)

clean = ctrl.Antecedent(x, 'clean_code')
func = ctrl.Antecedent(x, 'functionality')
inh = ctrl.Antecedent(x, 'inheritance')
success = ctrl.Consequent(x, 'project_success')

# -----------------------------
# 2. Membership Functions (Simple & Smooth)
# -----------------------------
# Clean code
clean['low']    = fuzz.trapmf(x, [0, 0, 20, 45])
clean['medium'] = fuzz.trimf(x, [30, 50, 70])
clean['high']   = fuzz.trapmf(x, [55, 80, 100, 100])

# Functionality
func['very_low'] = fuzz.trapmf(x, [0, 0, 10, 25])
func['low']      = fuzz.trimf(x, [15, 35, 55])
func['medium']   = fuzz.trimf(x, [45, 60, 75])
func['high']     = fuzz.trapmf(x, [65, 80, 100, 100])

# Inheritance
inh['low']    = fuzz.trapmf(x, [0, 0, 20, 45])
inh['medium'] = fuzz.trimf(x, [35, 55, 75])
inh['high']   = fuzz.trapmf(x, [65, 80, 100, 100])

# Output: Project Success
success['very_poor'] = fuzz.trapmf(x, [0, 0, 10, 20])
success['poor']      = fuzz.trimf(x, [15, 30, 45])
success['average']   = fuzz.trimf(x, [40, 55, 70])
success['good']      = fuzz.trimf(x, [60, 75, 90])
success['very_good'] = fuzz.trapmf(x, [85, 92, 100, 100])

# -----------------------------
# 3. Define the 36 Rules
# -----------------------------
rules = []

C = clean
F = func
I = inh
S = success

# HIGH CLEAN
rules.append(ctrl.Rule(C['high'] & F['high'] & I['high'], S['very_good']))
rules.append(ctrl.Rule(C['high'] & F['high'] & I['medium'], S['very_good']))
rules.append(ctrl.Rule(C['high'] & F['high'] & I['low'], S['good']))

rules.append(ctrl.Rule(C['high'] & F['medium'] & I['high'], S['good']))
rules.append(ctrl.Rule(C['high'] & F['medium'] & I['medium'], S['good']))
rules.append(ctrl.Rule(C['high'] & F['medium'] & I['low'], S['average']))

rules.append(ctrl.Rule(C['high'] & F['low'] & I['high'], S['average']))
rules.append(ctrl.Rule(C['high'] & F['low'] & I['medium'], S['average']))
rules.append(ctrl.Rule(C['high'] & F['low'] & I['low'], S['poor']))

rules.append(ctrl.Rule(C['high'] & F['very_low'] & I['high'], S['poor']))
rules.append(ctrl.Rule(C['high'] & F['very_low'] & I['medium'], S['poor']))
rules.append(ctrl.Rule(C['high'] & F['very_low'] & I['low'], S['very_poor']))

# MEDIUM CLEAN
rules.append(ctrl.Rule(C['medium'] & F['high'] & I['high'], S['very_good']))
rules.append(ctrl.Rule(C['medium'] & F['high'] & I['medium'], S['good']))
rules.append(ctrl.Rule(C['medium'] & F['high'] & I['low'], S['good']))

rules.append(ctrl.Rule(C['medium'] & F['medium'] & I['high'], S['good']))
rules.append(ctrl.Rule(C['medium'] & F['medium'] & I['medium'], S['average']))
rules.append(ctrl.Rule(C['medium'] & F['medium'] & I['low'], S['average']))

rules.append(ctrl.Rule(C['medium'] & F['low'] & I['high'], S['average']))
rules.append(ctrl.Rule(C['medium'] & F['low'] & I['medium'], S['poor']))
rules.append(ctrl.Rule(C['medium'] & F['low'] & I['low'], S['poor']))

rules.append(ctrl.Rule(C['medium'] & F['very_low'] & I['high'], S['poor']))
rules.append(ctrl.Rule(C['medium'] & F['very_low'] & I['medium'], S['very_poor']))
rules.append(ctrl.Rule(C['medium'] & F['very_low'] & I['low'], S['very_poor']))

# LOW CLEAN
rules.append(ctrl.Rule(C['low'] & F['high'] & I['high'], S['good']))
rules.append(ctrl.Rule(C['low'] & F['high'] & I['medium'], S['average']))
rules.append(ctrl.Rule(C['low'] & F['high'] & I['low'], S['average']))

rules.append(ctrl.Rule(C['low'] & F['medium'] & I['high'], S['average']))
rules.append(ctrl.Rule(C['low'] & F['medium'] & I['medium'], S['poor']))
rules.append(ctrl.Rule(C['low'] & F['medium'] & I['low'], S['poor']))

rules.append(ctrl.Rule(C['low'] & F['low'] & I['high'], S['poor']))
rules.append(ctrl.Rule(C['low'] & F['low'] & I['medium'], S['poor']))
rules.append(ctrl.Rule(C['low'] & F['low'] & I['low'], S['very_poor']))

rules.append(ctrl.Rule(C['low'] & F['very_low'] & I['high'], S['very_poor']))
rules.append(ctrl.Rule(C['low'] & F['very_low'] & I['medium'], S['very_poor']))
rules.append(ctrl.Rule(C['low'] & F['very_low'] & I['low'], S['very_poor']))

# -----------------------------
# 4. Build System (EXPORT THIS)
# -----------------------------
system_ctrl = ctrl.ControlSystem(rules)

# -----------------------------
# 5. Optional Test Block
# -----------------------------
if __name__ == "__main__":
    sim = ctrl.ControlSystemSimulation(system_ctrl)

    sim.input['clean_code'] = 67
    sim.input['functionality'] = 34
    sim.input['inheritance'] = 100

    sim.compute()
    print("Project success (crisp):", sim.output['project_success'])

    clean.view()
    plt.title("Clean Code Membership Functions")
    plt.show()

    func.view()
    plt.title("Functionality Membership Functions")
    plt.show()

    inh.view()
    plt.title("Inheritance Membership Functions")
    plt.show()

    success.view()
    plt.title("Project Success Membership Functions")
    plt.show()
