atmodel
=======

This project is under Professor Philip Lubin. This program is to facilitate the analysis of telescope observation data in various sites on different sources. 

There are a large amount of excel files that make the analysis very cubersome to work with. This program organizes the information of different excel files and allows user to specify the information and automatically produce the whatever data user needed in a new excel file.

=======

The program contains following files (only .py files are program files):

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

numpy/scipy: for calculation

xlrd/xlwt: for excel accessing. see python-excel

matplotlib: for plotting

In order to run the program please make sure these packages are properly installed.

