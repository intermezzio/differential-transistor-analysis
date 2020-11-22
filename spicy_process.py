import numpy as np
import pandas as pd

def load_spice(spice_file, index_name="index"):
	"""
	Read a spice file from LTSpice
	"""
	# load the file as a dataframe
	raw_csv = pd.read_csv(spice_file,
		delimiter="\\s+", error_bad_lines=False
	).reset_index(col_fill=index_name)

	# if it's just one line with data
	if raw_csv.shape[0] == 0:
		raw_data = pd.DataFrame({"index": raw_csv.columns[1:]})
		raw_data["Run"] = 1
		raw_data = raw_data.apply(
			lambda col:pd.to_numeric(col, errors='ignore')
		)
		return raw_data

	# split data by runs
	try:
		run_indices = np.where(raw_csv.iloc[:,0].str.contains("Step"))[0]
	except AttributeError:
		# no runs
		raw_csv["Run"] = 1
		return raw_csv

	csv_by_run = np.array_split(
		raw_csv,
		run_indices
	)
	del raw_csv

	# combine data for each test run
	summative_df = None
	for i, df in enumerate(csv_by_run):
		df["Run"] = i
		# delete text row
		df = df.iloc[1:]

		# merge all runs together
		if i==0:
			summative_df = df
		else:
			summative_df = summative_df.append(df, ignore_index=True)
	
	# convert data to numbers
	summative_df = summative_df.apply(
		lambda col:pd.to_numeric(col, errors='ignore')
	)

	return summative_df

if __name__ == "__main__":
	df = load_spice("../Lab0/HW2.txt")