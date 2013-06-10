
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
        self.row_start = int((freq_start - self.freq_offset)/self.freq_step_size) + self.row_offset
        self.row_end = int((freq_end - self.freq_offset) / self.freq_step_size)+ 1 + self.row_offset

    def set_freq_range_Hz(self, freq_start, freq_end):
        self.freq_offset *= 3 * 10 ** 10
        self.freq_step_size *= 3 * 10 ** 10
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


