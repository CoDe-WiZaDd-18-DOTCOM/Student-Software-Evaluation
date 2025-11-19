import os
import javalang

class CodeMetrics:
    def __init__(self):
        self.loc = 0
        self.num_classes = 0
        self.num_methods = 0
        self.inheritance_depth = 0
        self.overrides = 0
        self.total_cc = 0  # cyclomatic complexity estimate

def estimate_java_complexity(code):
    # Very simple rule-based complexity estimation
    keywords = ["if", "for", "while", "case", "catch", "&&", "||"]
    count = 1
    for k in keywords:
        count += code.count(k)
    return count

def extract_java_metrics(path):
    metrics = CodeMetrics()

    for root, _, files in os.walk(path):
        for f in files:
            if f.endswith(".java"):
                file_path = os.path.join(root, f)
                with open(file_path, "r", encoding="utf-8", errors="ignore") as file:
                    code = file.read()
                    metrics.loc += len(code.splitlines())

                    # estimated complexity
                    metrics.total_cc += estimate_java_complexity(code)

                    try:
                        tree = javalang.parse.parse(code)
                    except:
                        continue

                    # classes
                    for _, node in tree.filter(javalang.tree.ClassDeclaration):
                        metrics.num_classes += 1
                        if node.extends:
                            metrics.inheritance_depth += 1

                    # overridden methods
                    for _, node in tree.filter(javalang.tree.MethodDeclaration):
                        metrics.num_methods += 1
                        if node.annotations:
                            for ann in node.annotations:
                                if "Override" in str(ann):
                                    metrics.overrides += 1

    return metrics


def compute_fuzzy_inputs(m):
    # CLEAN CODE
    clean_code = 100
    clean_code -= min(50, m.total_cc * 1.2)
    clean_code -= min(20, m.num_methods * 0.3)
    clean_code = max(0, min(100, clean_code))

    # FUNCTIONALITY
    functionality = m.num_methods * 2 + m.num_classes * 3
    functionality = min(100, functionality)

    # INHERITANCE
    inheritance = m.inheritance_depth * 25 + m.overrides * 5
    inheritance = min(100, inheritance)

    return clean_code, functionality, inheritance
