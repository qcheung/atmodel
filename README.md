atmodel
=======

This project is under Professor Philip Lubin. This program is to facilitate the analysis of telescope observing in various sites on different sources. 

There are a large amount of excel files that make the analysis very cubersome to work with. This program organize the information of different excel files and produce the data needed in a new excel files as the user specify. 

=======

The program contains following files:

atmodel.py

It controls the User Interface and main program loop

excel.py

It contains two classes to help excel reading and writing: ExcelReader and ExcelWriter.

plotter.py

It's a collection of functions related to plotting graphs of data

cal.py

It contains functions for detailed calculations

exceptions.py

It deals with exceptions in the program. Currently remains undeveloped

const.py

It contains all constant definitions. 

========

Packages used:

Wxpython: for UI
numpy/simpy: for calculation
xlrd/xlwt: for excel accessing. see python-excel
matplotlib: for plotting

In order to run the program please make sure these packages are properly installed.

