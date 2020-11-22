from analyze import *
from spicy_process import load_spice

import numpy as np
import pandas as pd

## Load and Sanitize Data
data = load_spice("data/Exp1.txt")
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

## Filter Data
data = data[data["V1-V2"].abs() < 0.15]

## Plot
fig, ax = plt.subplots(figsize=(10,8))

for i, (run, df) in enumerate(data.groupby("Run")):
	print(run)
	plot_theoretical(df["V1-V2"], df["I1-I2"], ax=ax, label=f"{v2_vals[run-1]}V")
	plot_experimental(df.loc[df.index % 3 == i,"V1-V2"], df.loc[df.index % 3 == i,"I1-I2"], ax=ax, label=f"{v2_vals[run-1]}V")
	# ax.plot(df.loc[(run-1)::3,"V1-V2"], df.loc[(run-1)::3,"I1-I2"], ".", label=f"V2={v2_vals[run-1]}V", alpha=0.6)

ax.set_title("Current versus Voltage Across a Differential Pair of Transistors")
ax.set_xlabel("V1-V2 (V)")
ax.set_ylabel("I1-I2 (A)")
fig.legend(loc="lower right")
fig.savefig("plot4.png")
fig.savefig("plot4.eps")
plt.show()