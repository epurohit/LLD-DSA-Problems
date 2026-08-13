"""
Problem Statement: Agentic Workflow Scheduler
You are building the execution engine for an internal AI agent. The agent generates a workflow consisting of multiple tasks. Each task has a unique ID and a list of other task IDs that must be completed before it can start.

Your goal is to write a function that takes this workflow and returns a valid execution schedule. To minimize total execution time, your schedule must group tasks into "batches" that can be executed in parallel.

If the agent hallucinates a circular dependency (e.g., Task A depends on Task B, and Task B depends on Task A), your system must detect it and raise a ValueError.
"""

from collections import defaultdict, deque

def schedule_workflow(tasks: dict[str, list[str]]) -> list[list[str]]:
    """
    Calculates the optimal parallel execution schedule for a set of dependent tasks.
    
    :param tasks: A dictionary where the key is the task ID, and the value is a 
                  list of task IDs that must run first (dependencies).
    :return: A list of lists representing batches of parallelizable tasks.
    :raises ValueError: If a circular dependency is detected.
    """
    visited = 0
    task_dependents = defaultdict(list)
    in_degree = defaultdict(int)
    task_queue = deque()

    for task, task_dependencies in tasks.items():
        in_degree[task] = len(task_dependencies)
        for dep_task in task_dependencies:
            task_dependents[dep_task].append(task)

    for task, num_deps in in_degree.items():
        if (num_deps==0):
            task_queue.append(task)

    ans = list()
    while task_queue:
        num_tasks = len(task_queue)
        curr_batch = list()

        for _ in range(num_tasks):
            curr_task = task_queue.popleft()
            for task in task_dependents[curr_task]:
                in_degree[task] -= 1
                if (in_degree[task] == 0):
                    task_queue.append(task)

            curr_batch.append(curr_task)
            visited += 1

        ans.append(curr_batch)

    if visited != len(tasks):
        raise ValueError("Cyclic Dependency Found")

    return ans
