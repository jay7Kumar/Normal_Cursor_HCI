import openpyxl
import os
from openpyxl import workbook


class RecordDataToExcel:
    def __init__(self):
        self._file_path = "/Users/mercurius/PycharmProjects/normalPointer/data1.xlsx"

    def write_to_excel(self, data_row):
        if not os.path.isfile(self._file_path):  # no file with the name "data.xlsx"
            print("no file")
            data_wb = openpyxl.Workbook()  # create a file
            data_wb.save(self._file_path)
        else:
            data_wb = openpyxl.load_workbook(self._file_path)  # open the file

        data_sheet = data_wb.active
        data_sheet.append(data_row)  # append data to the end of the file
        data_wb.save(self._file_path)  # save the file
