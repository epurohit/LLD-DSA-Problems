from main import schedule_workflow

# Test Case 1: Linear & Parallel mix
workflow_1 = {
    "A": [],           # A has no dependencies
    "B": ["A"],        # B needs A
    "C": ["A"],        # C needs A
    "D": ["B", "C"],   # D needs B and C
    "E": []            # E has no dependencies
}

print(schedule_workflow(workflow_1))

# Expected Output: 
# [
#   ["A", "E"],   # A and E can start immediately
#   ["B", "C"],   # B and C can start after A finishes
#   ["D"]         # D must wait for B and C
# ]
# Note: Order within the inner lists does not matter.

# Test Case 2: Deep Chain
workflow_2 = {
    "Task1": [],
    "Task2": ["Task1"],
    "Task3": ["Task2"],
    "Task4": ["Task3"]
}

print(schedule_workflow(workflow_2))
# Expected Output: [["Task1"], ["Task2"], ["Task3"], ["Task4"]]

# Test Case 3: Circular Dependency (Agent Hallucination)
workflow_3 = {
    "DataFetch": ["Analysis"],
    "Analysis": ["Format"],
    "Format": ["DataFetch"] 
}

try:
    print(schedule_workflow(workflow_3))
except ValueError as e:
    print(str(e))
# Expected Output: Raises ValueError

# Test Case 4: Partial Circular Dependency (Agent Hallucination)
workflow_4 = {
    "T1": [],
    "T2": ["T3"],
    "T3": ["T2"] 
}

try:
    print(schedule_workflow(workflow_4))
except ValueError as e:
    print(str(e))

# Expected Output: Raises ValueError