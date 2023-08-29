#!/usr/bin/env python3
# main_script.py
import params
import subprocess

def run_target_script(iterations):
    processes = []
    for i in range(1,iterations + 1):
        print(f"Running iteration {i}")
        process = subprocess.Popen(["python", "node.py", str(i)])
        processes.append(process)
        print()

    # Wait for all child processes to finish
    for process in processes:
        process.wait()

if __name__ == "__main__":
    num_iterations = params.number_of_nodes  # Change this value to the number of times you want to run the script.
    run_target_script(num_iterations)