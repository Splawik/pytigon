import subprocess
from pytigon.pytigon_run import run


with open("js_requirements.txt", "rt") as f:
    requirements = f.read().splitlines()

for requirement in requirements:
    if requirement.startswith("#") or not requirement.strip() or ".css" in requirement:
        continue
    print(f"Installing {requirement}...")
    # subprocess.check_call(["./aube", "add", requirement])

    ret = run(
        ["ptig", "@aube", "add", requirement, "--silent", "--allow-low-downloads"]
    )

print("All dependencies installed successfully.")
