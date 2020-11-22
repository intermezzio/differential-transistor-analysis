from analyze import *
from spicy_process import load_spice

import numpy as np
import pandas as pd

## Load and Sanitize Data
data = load_spice("data/Exp1pt2.txt")
data = data.rename(columns={
		"level_0": "V1-V2",
		"level_1": "I1",
		"v2": "I2"
	})
del data["I(I1)"]
del data["I(I2)"]

data["I1+I2"] = data["I1"] + data["I2"]
data["I1-I2"] = data["I1"] - data["I2"]

v2_vals = [2.5, 3.5, 4.5]

## Plot
fig, ax = plt.subplots(figsize=(10,8))

for run, df in data.groupby("Run"):
	print(run)
	for yaxis in ("I1", "I2", "I1+I2", "I1-I2"):
		ax.plot(df.loc[df.index % 3 == run-1,"V1-V2"], df.loc[df.index % 3 == run-1,yaxis], ".", label=f"{yaxis}, V2={v2_vals[run-1]}V", alpha=0.6)

ax.set_title("Currents Across a Differential Pair of Transistors as a Function of Voltage Difference")
ax.set_xlabel("V1-V2 (V)")
ax.set_ylabel("Current (A)")
fig.legend(loc="lower right")
fig.savefig("plot5.png")
fig.savefig("plot5.eps")
plt.show()