from xlrd import open_workbook
from xlwt import Workbook
from xlsxwriter.workbook import Workbook
import os

#to read excel files
class ExcelReader:
    def __init__(self, file_location):
        self.book = open_workbook(file_location, on_demand = True)
        self.sheet = self.book.sheet_by_index(0)
        self.row_offset = 1
        self.col_offset = 0
        self.freq_offset = 0.05
        self.freq_step_size = 0.1
        
    def read_from_col(self, col):
        result = []
        for row in range(self.row_start, self.row_end):
            value = self.sheet.cell(row, col).value
            result.append(value)
        return result
    
    def set_freq_range(self, freq_start, freq_end):
        ## Note: we can determine whether or not our allowed range of frequencies is completely
        ##       outside the range of data by checking Row_End < Row_Start;
        ##       if Row_End < Row_Start, that means we don't have any data in the file within our
        ##       specified range of frequencies
        ####
        Row = self.row_offset #the first row we will test is the one following the rows skipped
        Current_Value = self.sheet.cell(Row, 1).value #this is the value from column 1 of the "Row" above

        #NOTE: this technique for determining rows to start and stop reading from assumes the columns have values in ascending order

        #look for the first row to read from by going through the data and finding the first value greater than or equal to the starting frequency
        while Current_Value < freq_start: #search through frequency column until we find the frequency we want to start at(the first frequency greater than what we enter)
            Row = Row + 1 #if the row we look at is smaller than what we want, we go to the next row
            Current_Value = self.sheet.cell(Row, 1).value
        self.row_start = Row #the row we want to start reading from is the first row with a value that isn't less than the starting frequency we want

        #now that we have determined what value row to start reading from, we use the same technique to determine what row to terminate reading from
        while Current_Value <= freq_end: #search through column until we find the frequency we want to end at(the first frequency greater than what we enter)
            #inlcuding the equal sign establishes an inclusive range if one of the cells is equal to the desired ending frequency
            Row = Row + 1
            Current_Value = self.sheet.cell(Row, 1).value
        self.row_end = Row - 1 #the row we want to end reading from is the last row the while loop iterated through which is one less than the "Row" it will give

        print("row start is " + str(self.row_start))
        print("row end is " + str(self.row_end))

    def set_freq_range_Hz(self, freq_start, freq_end):
        self.freq_offset *= 3e10 #1.5e9
        self.freq_step_size *= 3e10 #3e9
        self.set_freq_range(freq_start, freq_end)

#to generate XLS excel format
class ExcelWriter:
    def __init__(self, path):
        self.path = path
        self.book = Workbook()
        self.sheet = self.book.add_sheet('Sheet1')
        self.column_to_fill = 0
        
    def write_col(self, column_name, column_content):
        row = 0
        self.sheet.write(row, self.column_to_fill, column_name)
        row += 1
        for x in column_content:
            self.sheet.write(row, self.column_to_fill, x)
            row += 1
        self.column_to_fill += 1
    def save(self):
        self.book.save(self.path)

#to generate XLSX format excel format
class ExcelXWriter:
    def __init__(self, path):
        self.path = path
        self.book = Workbook(path)
        self.sheet = self.book.add_worksheet()
        self.column_to_fill = 0
        
    def write_col(self, column_name, column_content):
        row = 0
        self.sheet.write(row, self.column_to_fill, column_name)
        row += 1
        for x in column_content:
            self.sheet.write(row, self.column_to_fill, x)
            row += 1
        self.column_to_fill += 1
    # write_note(self, note):
    def save(self):
        self.book.close()


