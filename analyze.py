import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

def plot_preconfig(ax, ftype):
	"""
	configure plot to loglog / semilog as necessary

	"""
	ax = ax if ax else plt

	# log / semilog scales
	if ftype == "exp":
		ax.set_yscale("log")
	elif ftype == "loglog":
		ax.set_xscale("log")
		ax.set_yscale("log")

def plot_data(xs, ys=None, f=None, ax=None, scatter=True, label="", ftype="linear", **kwargs):
	if ax == None:
		return
		
	if ys is None:
		ys = [f(x) for x in xs]

	if scatter:
		ax.scatter(xs, ys, label=label, **kwargs)
	else:
		ax.plot(xs, ys, label=label, **kwargs)

def plot_postconfig(ax, xlabel="", ylabel="", title=""):
	"""
	Set axis and title labels here
	"""
	ax.set_xlabel(xlabel)
	ax.set_ylabel(ylabel)
	ax.set_title(title)


def get_curve_fit(xs, ys, f):
	# fit xs to ys via function f
	popt, _ = curve_fit(f, xs, ys)
	return popt

def plot_theoretical(xs, ys, ftype="linear", func=None, f_str=None, ax=None, label="", **kwargs):
	# decide on the function for the curve fit
	ys_test = ys
	if ftype == "linear":
		f = lambda x, m, b: m*x + b
		f_str = "y = {} * x + {}"
	elif ftype == "exp":
		f = lambda x, a, b: a * x + b
		ys_test = np.log(ys_test)
		f_str = "ln(y) = {} * x + {}"
	elif ftype == "loglog":
		f = lambda x, a, b: a * np.log(x) + b
		ys_test = np.log(ys_test)
		f_str = "ln(y) = {} * ln(x) + {}"
	else:
		f = func

	# do the curve fit
	params = get_curve_fit(xs, ys_test, f)
	if f_str:
		print(f_str.format(*params))

	if ftype == "linear":
		pass
	elif ftype == "exp":
		f = lambda x, a, b: np.exp(a * x + b)
	elif ftype == "loglog":
		f = lambda x, a, b: np.exp(a * np.log(x) + b)
	else:
		pass
	# plot theoretical
	plot_data(xs, f=lambda x: f(x, *params), label=label, ax=ax, scatter=False, **kwargs)

	return params

def plot_experimental(xs, ys, ax=None, label="", **kwargs):
	kwargs["marker"] = kwargs.pop("marker", "o")
	# plot experimental
	plot_data(xs, ys=ys, label=label, ax=ax, **kwargs)

def model_axes(datasets, ax=None):
	"""
	datasets is a dictionary:
	list of data
	[{xs, ys, label}, ...]

	ftype
	pltargs
		xlabel, ylabel, title, etc
	"""
	print(f"{datasets['name']}:\n\n")

	# set log axes
	plot_preconfig(ftype=datasets["ftype"], ax=ax)

	# everything goes on one axis
	for dataset in datasets["data"]:
		dataset["kwargs"] = dataset["kwargs"] if "kwargs" in dataset.keys() else dict()
		plot_experimental(xs=dataset["xs"], ys=dataset["ys"], label=dataset["label"], ax=ax, **dataset["kwargs"])

	print(datasets)
	all_xs = np.concatenate([dataset["xs"] for dataset in datasets["data"]])
	all_ys = np.concatenate([dataset["ys"] for dataset in datasets["data"]])

	plot_theoretical(xs=all_xs, ys=all_ys, ax=ax, func=datasets["func"] if "func" in datasets.keys() else None,
		ftype=datasets["ftype"], label=datasets["name"],
		f_str=datasets["f_str"] if "f_str" in datasets.keys() else None,
		**datasets["pltargs"]
	)


def model_all(datasets_list):
	# iterate over dataset list and plot a new figure for each
	for i, datasets in enumerate(datasets_list):
		if "fig" in datasets.keys() and "ax" in datasets.keys():
			fig = datasets["fig"]
			ax = datasets["ax"]
		else:
			fig = plt.figure(i)
			ax = fig.add_subplot(111)
		model_axes(datasets, ax=ax)
		fig.legend()
		fig.savefig(f"{datasets['name']}.svg")
		fig.savefig(f"{datasets['name']}.png")
