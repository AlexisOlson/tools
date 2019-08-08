"""
Run given lc0 benchmark command a configurable number of times and process its reported nps.
"""


import sys
import re
import subprocess
import numpy as np


def usage():
    print(
        "Usage: {} [number of runs] [lc0 benchmark command + flags]".format(sys.argv[0]))
    sys.exit(1)


if len(sys.argv) < 3:
    usage()

try:
    num_runs = int(sys.argv[1])
except:
    usage()

nps = np.zeros(num_runs)

prog = re.compile(
    r".*Benchmark final time \S+ calculating (\d+) nodes per second.*", flags=re.DOTALL)

for i in range(num_runs):
    output = subprocess.check_output(
        sys.argv[2:], stderr=subprocess.STDOUT, universal_newlines=True)

    match = re.match(prog, output)

    if match:
        x = int(match.group(1))
        nps[i] = x

        print("[{}/{}] {} nps".format(i+1, num_runs, x))
    else:
        usage()

"""
Print statistics.
"""

print()
print("{:<10}{:.0f}".format("min", np.min(nps)))
print("{:<10}{:.0f}".format("max", np.max(nps)))
print("{:<10}{:.0f}".format("stddev", np.std(nps)))
print("{:<10}{:.0f}".format("mean", np.mean(nps)))
print("{:<10}±{:.0f}".format(
    "95% CI", 1.96*np.std(nps)/np.sqrt(num_runs)))  # All distributions are Gaussian, right?
