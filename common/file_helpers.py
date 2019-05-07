import os

import xlwt


def make_parent_folders(filename):
    dirname = os.path.dirname(filename)
    if not os.path.exists(dirname):
        os.makedirs(dirname)


def export_data_to_xls(filename, headers, data, transformer=None, sheet_name=None, ordinal_number=None, footers=None):
    if sheet_name is None:
        sheet_name = 'Sheet 1'

    # ensure folder to store exported xls
    make_parent_folders(filename)

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet(sheet_name)

    offset = 0

    # first column for ordinal number if required
    if ordinal_number is not None:
        offset = 1
        ws.write(0, 0, ordinal_number)

    # headers
    for col_num in range(len(headers)):
        ws.write(0, col_num + offset, headers[col_num])

    # data
    row_num = 1
    for row in data:
        # transform data if required
        if callable(transformer):
            row = transformer(row)

        # write ordinal number if required
        if ordinal_number is not None:
            ws.write(row_num, 0, row_num)

        # actual data
        for col_num in range(len(row)):
            ws.write(row_num, col_num + offset, row[col_num])

        row_num += 1

    # footers if present
    if footers:
        for col_num in range(len(footers)):
            ws.write(row_num, col_num + offset, footers[col_num])

    wb.save(filename)
