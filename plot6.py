from analyze import *
from spicy_process import load_spice

import numpy as np
import pandas as pd

## Load and Sanitize Data
data = load_spice("data/Exp1V_vb1V.txt")
data = data.rename(columns={
		"level_0": "V1-V2",
		"level_1": "Vb"
	})
del data["level_2"]
del data["v2"]
del data["V(v)"]

v2_vals = [2.5, 3.5, 4.5]

## Plot
csfont = {'fontname':'Comic Sans MS'}

fig, ax = plt.subplots(figsize=(10,8))

for run, df in data.groupby("Run"):
	plot_experimental(df["V1-V2"], df["Vb"], ax=ax, label=f"V2={v2_vals[run-1]}V")

ax.set_title("Source Node Voltage as a function of the Differences of Voltages in a Differenital Pair of Transistors")
ax.set_xlabel("V1-V2 (V)")
ax.set_ylabel("Source Node Voltage (V)")
fig.legend(loc="lower right")
fig.savefig("plot6.png")
fig.savefig("plot6.eps")
plt.show()