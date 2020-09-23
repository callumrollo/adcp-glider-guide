These scripts will produce QC plots from snipped files of a NOrtek 1 MHz AD2CP integrated on a Konsgberg Seaglider

Both files must be present in the same directory (though this does not have to be the directory where the input files are)

To produce the QC images, call the python script tele_checker.py. You will need Python 3.6 or better. You can pass the path to the telemetry script as an optional argument. Otherwise the script will use the current working directory.

Figures are written to the current working directory. Figures are not remade by default (expcept for the average plots) to force reprocessing of old plots, simnply remove the plots.
