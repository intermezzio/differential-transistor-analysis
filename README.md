# Circuits Lab 7
This is the seventh lab in my Introduction to Microelectronic Circuits class at Olin College. This lab studies the behavior of a differential pair of circuits.  

## File Structure
The data folder has text output from LTSpice experiments. All of the python scripts to generate plots are in the root directory.

## Usage
This series of scripts depends on Python3, as well as numpy, matplotlib, scipy, and pandas. All required packages are in the `requirements.txt` file.  
First install these dependencies
```sh
pip install -r requirements.txt
```

Then run plot#.py, where each # is a number for the figure number you need to generate. This should generate a png and eps file of the figure. For example, to generate figure 2:

```sh
python plot2.py
```

## How it Works
The `spicy_process.py` script imports an LTSpice text file and converts it into a Pandas DataFrame. This data is processed and plotted in the plot scripts. The plotting and curve fitting is further automated with the `analyze.py` script, which works as a frontend to matplotlib and scipy, generating linear, exponential, and log-log plots as well as curve fits on given data.
