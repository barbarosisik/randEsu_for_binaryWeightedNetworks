import subprocess

#scripts to run
scripts = [
    "weighted_rand_esu_eval.py",
    "initial_rand_esu_eval.py",
    "combined_plot.py"
]

for script in scripts:
    print(f"Running {script}...")
    subprocess.run(["python", script], check=True)
    print(f"{script} completed successfully.\n")

print("All scripts executed successfully.")
