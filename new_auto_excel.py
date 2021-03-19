import openpyxl
import os
import sys
from openpyxl import load_workbook   # 读取表的模块

base_path = sys.path[0] + '\\周数据表\\'
finaly_workbook = load_workbook(sys.path[0] + '\\表格\\周平衡计分卡.xlsx')


# take all tables
def take_tables(base_path):
    dirs = os.listdir(base_path)
    dir_sheetdir = []
    for dir in dirs:
        names = os.listdir(base_path + dir)
        sheetdir_tables = []
        for name in names:
            table = load_workbook(base_path + dir + "\\"+name)
            sheetdir_tables.append(table)
        dir_sheetdir.append(sheetdir_tables)

    return dir_sheetdir


# the review_data
def table_to_sheet(tables, finaly_table_sheet):
    for table in tables:
        # take the sheet
        table_sheet = table[table.sheetnames[0]]

        for i in range(1, finaly_table_sheet.max_row + 1):
            for j in range(1, table_sheet.max_row + 1):
                for k in range(1, table_sheet.max_column + 1):

                    # if the cell is empty, fill it with 0
                    if not table_sheet.cell(row=j, column=k).value:
                        table_sheet.cell(row=j, column=k, value=0)

                    # 判断总表的字段与审核概况表字段是否相同，相同则将分表数据填入总表中
                    if finaly_table_sheet.cell(row=i, column=1).value == table_sheet.cell(row=j, column=1).value and finaly_table_sheet.cell(row=i, column=2).value == table_sheet.cell(row=1, column=k).value:
                        finaly_table_sheet.cell(
                            row=i, column=3, value=table_sheet.cell(row=j, column=k).value)


# the AI_data
def table_to_AIsheet(tables, finaly_table_sheet):
    table0_sheet = tables[0][tables[0].sheetnames[0]]
    table1_sheet = tables[1][tables[1].sheetnames[0]]

    for i in range(1, finaly_table_sheet.max_row+1):
        for j in range(1, table1_sheet.max_row+1):
            for k in range(1, table1_sheet.max_column+1):
                if finaly_table_sheet.cell(row=i, column=2).value == table1_sheet.cell(row=j, column=2).value and finaly_table_sheet.cell(row=i, column=3).value == table1_sheet.cell(row=1, column=k).value:
                    finaly_table_sheet.cell(
                        row=i, column=5, value=table1_sheet.cell(row=j, column=k).value)

        for n in range(1, table0_sheet.max_column+1):
            if finaly_table_sheet.cell(row=i, column=3).value == table0_sheet.cell(row=1, column=n).value:
                finaly_table_sheet.cell(
                    row=i, column=5, value=table0_sheet.cell(row=2, column=n).value)

        if not finaly_table_sheet.cell(row=i, column=5).value:
            finaly_table_sheet.cell(
                row=i, column=5, value=finaly_table_sheet.cell(row=i, column=4).value)


# the main
def main():
    # 读取汇总表的三个sheet
    sheet1_finaly_workbook = finaly_workbook[finaly_workbook.sheetnames[0]]
    sheet2_finaly_workbook = finaly_workbook[finaly_workbook.sheetnames[1]]
    sheet3_finaly_workbook = finaly_workbook[finaly_workbook.sheetnames[2]]

    # take the table for filanySheet
    all_tables = take_tables(base_path)
    sheet1_excels = all_tables[0]
    sheet2_excels = all_tables[1]
    sheet3_excels = all_tables[2]

    # 开始匹配填表
    table_to_sheet(sheet1_excels, sheet1_finaly_workbook)
    print('sheet1填写保存完毕！！！')
    table_to_AIsheet(sheet2_excels, sheet2_finaly_workbook)
    print('sheet2填写保存完毕！！！')
    table_to_sheet(sheet3_excels, sheet3_finaly_workbook)
    print('sheet3填写保存完毕！！！')
    finaly_workbook.save(filename=sys.path[0] + '\\表格\\周平衡计分卡.xlsx')


if __name__ == "__main__":
    main()
    print('全部填写完成！')
