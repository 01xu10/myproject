# !/usr/bin/env python
# -*- coding: utf-8 -*-
''''''

'''
    1、处理Excel模块: openpyxl
         pip install openpyxl
'''


'''
    2、如何创建一个excel表格？
        A、导包
        B、在内存中创建一个表格
        C、将内存中的虚拟表格保存到本地！
'''
# from openpyxl import Workbook
# wb = Workbook()
# wb.save('first_create.xlsx')


'''
    3、如何打开一个已经存在的excel表格
        A、导包
        B、load_workbook(),返回值是一个对象，通过操作这个对象去操作表格
'''
# from openpyxl import load_workbook
# wb = load_workbook('first_create.xlsx')
#

'''
    4、如何获取，修改sheet的名字?
        1、获取当前活跃的工作表（sheet） --> 使用active方法
        2、使用sheet.title得到表名！
        3、所有的修改必须保存，不然都是在内存中修改！
'''
# from openpyxl import load_workbook
# wb = load_workbook('first_create.xlsx', data_only=True)
# sheet = wb.active
# sheet.title = '贝塔的花姑娘'
# print(sheet.title)
# wb.save('first_create.xlsx')


'''
    5、如何像excel表格中写数据（一个一个写）
        无则增，有则改
'''
# from openpyxl import load_workbook
# import datetime
# wb = load_workbook('first_create.xlsx', data_only=True)
# sheet = wb.active
# sheet['B3'] = '苍井空'
# sheet['C3'] = '18'
# sheet['D3'] = '170cm'
# sheet['E3'] = '88, 88, 88'
# sheet['F3'] = datetime.datetime.now().strftime('%Y-%m-%d')
# sheet['B3'] = '林志玲'
# wb.save('first_create.xlsx')


'''
    6、如何像excel表格中一次性写入多条数据？ --> 使用append()
        原则：默认是在写在有数据的行的下一行！
        data_only=True --> 只显示值，由于excel表格中，有很多公式，不显示公式，只显示值！ 
'''
# from openpyxl import load_workbook
# import datetime
# wb = load_workbook('first_create.xlsx', data_only=True)
# sheet = wb.active
# sheet.append(['三上悠亚', 18, '180cm', '90, 90, 90', datetime.datetime.now().strftime('%Y-%m-%d')])
# wb.save('first_create.xlsx')


'''
    7、获取所有的sheet名字
        sheetnames()
'''
# from openpyxl import load_workbook
# wb = load_workbook('员工工资表.xlsx', data_only=True)
# print(wb.sheetnames)


'''
    8、获取指定的活动表, 拿到活动表后，操作活动表
        get_sheet_by_name()  --> 这种方法会报警告错误！使用以下方法
        wb['表名']           --> <Worksheet "Sheet1">
'''
# from openpyxl import load_workbook
# wb = load_workbook('员工工资表.xlsx', data_only=True)
# sheet = wb['Sheet1']
# print(sheet)


'''
    9、获取指定表后，查询单元格数据   sheet['D1']返回的是一个单元格对象，通过value取值
        A、有数据就返回数据
        B、无数据就返回None
'''
# from openpyxl import load_workbook
# wb = load_workbook('员工工资表.xlsx', data_only=True)
# sheet = wb['Sheet1']
# data_D1 = sheet['D1']
# print(data_D1.value)
# data_GG1 = sheet['GG1']
# print(data_GG1.value)


'''
    10、循环遍历【使用切片方式】，获取单元格值 --> sheet['B1':'F1'] 
        返回值是一个元祖，里面有一个元祖，对其里面的元祖进行for循环，然后用value取值
'''
# from openpyxl import load_workbook
# wb = load_workbook('员工工资表.xlsx', data_only=True)
# sheet = wb['Sheet1']
# # print(sheet['B1':'F1'])
# for cell in sheet['B1': 'F1'][0]:
#     print(cell.value, end=' ')
#

'''
    11、按行遍历
        遍历思路：1、逐行遍历，每一行是一个元祖； 2、对每个行进行遍历，得到每个单元格，对单元格取值，得到结果
'''
# from openpyxl import load_workbook
# wb = load_workbook('员工工资表.xlsx', data_only=True)
# sheet = wb['Sheet1']
# for row in sheet:
#     for cell in row:
#         print(cell.value, end=' ')
#     print(' ')


'''
    12、按列遍历
        遍历思路：1、逐列遍历，每一列是一个元祖； 2、对每个列进行遍历，得到每个单元格，对单元格取值，得到结果
'''
# from openpyxl import load_workbook
# wb = load_workbook('员工工资表.xlsx', data_only=True)
# sheet = wb['Sheet1']
# for column in sheet.columns:
#     for cell in column:
#         print(cell.value, end=' ')
#     print(' ')


'''
    13、遍历指定行，指定列
        sheet.iter_rows, min_row, max_row, min_col, max_col
'''
# from openpyxl import load_workbook
# wb = load_workbook('员工工资表.xlsx', data_only=True)
# sheet = wb['Sheet1']
# for row in sheet.iter_rows(min_row=2, max_row=5, min_col=3, max_col=4):
#     for cell in row:
#         print(cell.value, end=' ')
#     print(' ')


'''
    14、设置单元格样式（导包部分）
          Font     ： 设置字体
          colors   ： 设置颜色
          Alignment： 设置文本对齐方式
          size     :  设置字体大小 
          italic   :  设置斜体
          bold     :  设置粗体
'''
# from openpyxl.styles import Font, colors, Alignment


'''
    15、设置字体样式
          1、声明样式：font_style = '样式内容';
          2、设置样式：sheet['D1'] = font_style
'''
# from openpyxl import load_workbook
# from openpyxl.styles import Font, colors, Alignment
# wb = load_workbook('员工工资表.xlsx')
# sheet = wb['Sheet1']
# sheet['D1'].font = Font(name='宋体', size=20, italic=True, color=colors.BLACK, bold=True)
# wb.save('员工工资表_01.xlsx')


'''
    16、设置对齐方式
'''
# from openpyxl import load_workbook
# from openpyxl.styles import Font, colors, Alignment
# wb = load_workbook('员工工资表.xlsx')
# sheet = wb['Sheet1']
# sheet['D1'].alignment = Alignment(horizontal='center', vertical='center')
# wb.save('员工工资表_01.xlsx')


'''
    17、设置单元格宽，高
        row_dimensions   , height
        column_dimensions, width
'''
# from openpyxl import load_workbook
# from openpyxl.styles import Font, colors, Alignment
# wb = load_workbook('员工工资表_01.xlsx')
# sheet = wb['Sheet1']
# # 设置第二行的行高
# sheet.row_dimensions[2].height = 30
# # 设置第三列的列宽
# sheet.column_dimensions['C'].width = 40
# wb.save('员工工资表_01.xlsx')

