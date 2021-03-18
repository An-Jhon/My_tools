from PIL import Image
import xlsxwriter
import numpy as np
import os


def rgbToHex(RGB):
    strs = '#'
    for num in RGB:
        strs += str(hex(num))[-2:].replace('x', '0').upper()
    return strs


picturs = os.listdir("C:/Users/v_yruian/Desktop/new/excel_drawing/picturs")

for pic in picturs:
    im = Image.open(
        "C:/Users/v_yruian/Desktop/new/excel_drawing/picturs/%s" % pic)
    imdata = im.getdata()  # 获取图片像素的RGB值，这个值是一个包含261*193个像素点（252,235,255）的数组对象
    imnp = np.array(imdata)  # 将数组对象转换成np数组（一个二维数组，维度是（261*193,3））
    imarray = imnp.reshape(im.size[1], im.size[0], 3)   # 改变数组形状

    pic_name = pic.split('.')
    wb = xlsxwriter.Workbook(
        "C:/Users/v_yruian/Desktop/new/excel_drawing/excels/%s.xlsx" % pic.split('.')[0])
    ws = wb.add_worksheet("image")

    ws.hide_gridlines(2)   # 隐藏线框
    # ws.hide_gridlines(2)
    # 参数0，不隐藏
    # 参数1，仅隐藏打印的网格线
    # 参数2，隐藏屏幕和打印的网格线

    ws.set_column(0, im.size[0], 0.1)
    # 2 ws.set_column(0,3,40) #设定第1到4列的列宽为40
    # 3 ws.set_column("A:A", 40) #设定A列列宽为40
    # 4 ws.set_column("B:D", 15) #设定B、C、D三列的列宽为15
    # 5 ws.set_column("E:F", 50) #设定E、F列的列宽为50

    for row, rowdata in enumerate(imarray):
        ws.set_row(row, 0.8)
        #  ws.set_row(0,40) #设置第一行的高度为40

        for col, coldata in enumerate(rowdata):
            ws.write(row, col, '', wb.add_format(
                {'bg_color': rgbToHex(list(coldata)), }))
    wb.close()

print('绘画完毕！')
