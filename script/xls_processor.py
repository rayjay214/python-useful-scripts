#!/usr/bin/env python
# coding=utf-8

import xlrd
from xlutils.copy import copy
    
def get_xl_for_read(name):
    workbook = xlrd.open_workbook(name)
    return workbook

def get_xl_for_write(workbook_r):
    workbook_cp = copy(workbook_r)
    return workbook_cp    

def xl_row_gen(sheet_r):
    rows = sheet_r.nrows
    for rowno in range(1, rows):
        row = sheet_r.row_values(rowno)
        if row:
            yield row,rowno

def process_xl(sheet_r, sheet_w):
    row_gen = xl_row_gen(sheet_r)
    while True:
        try:
            row,rowno = row_gen.__next__()
            #change the content for second col of first row
            if rowno == 1:
                sheet_w.write(rowno, 2, 'changed content')
                    
        except StopIteration:
            print("over or failed")
            break
    
if __name__ == '__main__': 
    wb_r = get_xl_for_read('xls_processor.xls')
    wb_cp = get_xl_for_write(wb_r)
    sheet_r0 = wb_r.sheet_by_index(0) 
    sheet_w0 = wb_cp.get_sheet(0)
    process_xl(sheet_r0, sheet_w0)
    wb_cp.save('xls_processor_new.xls')

