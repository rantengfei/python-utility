import xlwt, os
# import psycopg2
import io


# from sanic.response import raw
# 数据库连接参数


def export(data, out_put_path):
    '''
    :details: 使用xlwt插件简单封装json数据->execl表格
    :param data:
    :return:
    '''
    borrower_book = xlwt.Workbook()
    installment_book = xlwt.Workbook(encoding='utf-8')

    default_book_style = borrower_book.default_style
    default_book_style.font.height = 12 * 20

    header01 = xlwt.XFStyle()

    style_COL_AC = xlwt.XFStyle()

    # fonts
    font_bold = xlwt.Font()
    font_bold.name = '宋体'
    font_bold.height = 200
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
    al.wrap = xlwt.Alignment.WRAP_AT_RIGHT  # 自动换行
    wrap = xlwt.easyxf('align: wrap on')

    header01.font = font_bold
    header01.borders = borders
    header01.alignment = al
    header01.pattern = color01

    style_COL_AC.borders = borders
    style_COL_AC.alignment = al
    style_COL_AC.pattern = BG_COL_AC
    # excel内容写入
    for sheet_data in data.get('sheet'):
        installment_sheet = installment_book.add_sheet(sheet_data.get('title_name'))
        # 行高
        installment_sheet.row(0).height = 25 * 40
        sdata = sheet_data.get("data")
        # 确定栏位宽度
        col_width = []
        l = 1
        for j in sdata[0]:
            col_width.append(len_byte(j,l))
            l += 1

        # 设置栏位宽度，栏位宽度小于10时候采用默认宽度
        for i in range(len(col_width)):
            installment_sheet.col(i).width = 256 * (col_width[i] + 1)

        for i, v in enumerate(tuple([x.get('cn_des') for x in sheet_data.get('row_title_name')])):
            installment_sheet.write(0, i, v, header01)

        for i, v in enumerate(sdata):
            n = i + 1
            for j in range(0, len(sdata[i])):
                installment_sheet.row(n).height = 20 * 20
                installment_sheet.write(n, j, list(v.items())[j][1], style_COL_AC)


                # # 列宽
                # installment_sheet.col(2).width = 260 * 30
                # cur_file_path = os.path.dirname(os.path.realpath(__file__))
    output = io.BytesIO()
    installment_book.save(output)
    output.seek(0)
    out = output.getvalue()
    output.close()
    # 返回响应头是关键
    return out
    # return os.path.join(cur_file_path,out_put_path+'.xls')


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


# 获取字符串长度，一个中文的长度为2
def len_byte(value, i):
    length = len(value)
    utf8_length = len(value.encode('utf-8'))
    if i > 3:
        length = (utf8_length - length) / 2 + length / 2
    if length < 10:
        length = 10
    return int(length)
