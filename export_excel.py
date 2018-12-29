import datetime
from sanic import response
import xlwt
import xlrd
from xlrd import xldate_as_tuple


async def export(path, save_name, export_name, head_message, data):
    today_date = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
    wbk = xlwt.Workbook()
    sheet = wbk.add_sheet('Sheet1', cell_overwrite_ok=True)
    header01, style_COL_AC = excel_style()
    tall_style = xlwt.easyxf('font:height 400;')
    for k, v in enumerate(head_message):
        sheet.write(0, k, head_message[k], header01)
    for i in range(len(data)):
        sheet.row(i).set_style(tall_style)
        for key, item in enumerate(data[i]):
            sheet.write(i + 1, key, data[i][item], style_COL_AC)
            sheet.col(key).width = 240 * 20
    file_path = f"{path}{save_name}{str(today_date)}.xls"
    wbk.save(file_path)
    return await response.file(file_path,
                               mime_type='application/vnd.ms-excel',
                               headers={"Content-Disposition": "attachment; filename="+export_name+".xls"})

async def export_path(path, save_name, export_name, head_message, data):
    today_date = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
    wbk = xlwt.Workbook()
    sheet = wbk.add_sheet('Sheet1', cell_overwrite_ok=True)
    header01, style_COL_AC = excel_style()
    tall_style = xlwt.easyxf('font:height 400;')
    for k, v in enumerate(head_message):
        sheet.write(0, k, head_message[k], header01)
    for i in range(len(data)):
        sheet.row(i).set_style(tall_style)
        for key, item in enumerate(data[i]):
            sheet.write(i + 1, key, data[i][item], style_COL_AC)
            sheet.col(key).width = 240 * 20
    file_path = f"{path}{save_name}{str(today_date)}{export_name}.xls"
    wbk.save(file_path)
    return file_path

async def export_path_notime(path,export_name, head_message, data):
    wbk = xlwt.Workbook()
    sheet = wbk.add_sheet('Sheet1', cell_overwrite_ok=True)
    header01, style_COL_AC = excel_style()
    tall_style = xlwt.easyxf('font:height 400;')
    for k, v in enumerate(head_message):
        sheet.write(0, k, head_message[k], header01)
    for i in range(len(data)):
        sheet.row(i).set_style(tall_style)
        for key, item in enumerate(data[i]):
            sheet.write(i + 1, key, data[i][item], style_COL_AC)
            sheet.col(key).width = 240 * 20
    file_path = f"{path}{export_name}.xls"
    wbk.save(file_path)
    return file_path

def excel_style():
    header01 = xlwt.XFStyle()

    style_COL_AC = xlwt.XFStyle()

    # fonts
    font_bold = xlwt.Font()
    font_bold.name = '宋体'
    font_bold.height = 10 * 20
    font_bold.bold = True

    # borders
    borders = xlwt.Borders()
    borders.top = xlwt.Borders.THIN
    borders.bottom = xlwt.Borders.THIN
    borders.left = xlwt.Borders.THIN
    borders.right = xlwt.Borders.THIN

    # background
    badBG = xlwt.Pattern()
    badBG.pattern = badBG.SOLID_PATTERN
    badBG.pattern_fore_colour = 0x22

    # background2
    color01 = xlwt.Pattern()
    color01.pattern = badBG.SOLID_PATTERN
    color01.pattern_fore_colour = 0x29

    BG_COL_AC = xlwt.Pattern()
    BG_COL_AC.pattern = badBG.SOLID_PATTERN
    BG_COL_AC.pattern_fore_colour = 0xFF

    # alignment
    al = xlwt.Alignment()
    al.horz = xlwt.Alignment.HORZ_CENTER
    al.vert = xlwt.Alignment.VERT_CENTER
    al.wrap = xlwt.Alignment.WRAP_AT_RIGHT # 自动换行

    header01.font = font_bold
    header01.borders = borders
    header01.alignment = al
    header01.pattern = color01

    style_COL_AC.borders = borders
    style_COL_AC.alignment = al
    style_COL_AC.pattern = BG_COL_AC
    return header01, style_COL_AC

# 读取excel文件
def excel_table_byindex(file='file.xls', colnameindex=0, by_index=0):
    rbook = open_excel(file)
    sheet = rbook.sheet_by_index(by_index)
    rows = sheet.nrows
    cols = sheet.ncols
    all_content = []
    for i in range(rows):
        row_content = []
        for j in range(cols):
            ctype = sheet.cell(i, j).ctype  # 表格的数据类型
            cell = sheet.cell_value(i, j)
            if ctype == 2 and cell % 1 == 0:  # 如果是整形
                cell = int(cell)
            elif ctype == 3:
                # 转成datetime对象
                date = datetime.datetime(*xldate_as_tuple(cell, 0))
                cell = date.strftime('%Y-%m-%d %H:%M:%S')
            elif ctype == 4:
                cell = True if cell == 1 else False
            row_content.append(cell)
        all_content.append(row_content)
    return all_content


def open_excel(file='file.xls'):
    try:
        data = xlrd.open_workbook(file_contents=file)
        # data = xlrd.open_workbook(file)
        return data
    except Exception as e:
        print(e)
