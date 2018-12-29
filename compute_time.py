from dateutil import rrule
import datetime
# 算两个时间的月数
def months_calculte(begin,end):
    begin += '-01'
    end += '-01'
    d1 = datetime.datetime.strptime(begin,'%Y-%m-%d')
    d2 = datetime.datetime.strptime(end,'%Y-%m-%d')
    # d2 = datetime.date(2017, 4)
    months = rrule.rrule(rrule.MONTHLY, dtstart=d1, until=d2).count()
    return months

# 算两个时间的天数
def days_calculte(begin, end):
    begin = begin.split('-')
    end = end.split('-')
    d = int(begin[2])
    m = int(begin[1])
    y = int(begin[0])
    # difference in day
    dd = int(end[2])
    # difference in month
    dm = int(end[1])
    # difference in year
    dy = int(end[0])
    begind = datetime.date(y, m, d)
    endd = datetime.date(dy, dm, dd)
    return (endd - begind).days+1

#算年数
def years_calculte(begin,end):
    begin = int(begin)
    end = int(end)
    return  end-begin+1

#生成连续的日期
def dateRange(begin, end):
    ymd = "%Y-%m-%d"
    if len(begin) == 7:
        ymd = "%Y-%m"
    if len(begin) == 4:
        c = int(end) - int(begin)+1
        year = []
        for i in range(c):
            year.append(str(int(begin)+i))
        return sorted(year)
    dates = []
    dt = datetime.datetime.strptime(begin, ymd)
    date = begin[:]
    while date <= end:
        dates.append(date)
        dt = dt + datetime.timedelta(1)
        date = dt.strftime(ymd)
    return sorted(set(dates))


def date_parmas_check(params):
    if not params.get('time_kind'):
        return False,'请表明要查寻的时间格式!'
    if not params.get('start_time') or not params.get('end_time'):
        return False,'缺少时间范围!'
    if params.get('time_kind') == 'month' and (
        not len(params.get('start_time')) == 7 or not len(params.get('end_time')) == 7):
        return False,'按月统计时间范围有误!'
    if params.get('time_kind') == 'year' and (
        not len(params.get('start_time')) == 4 or not len(params.get('end_time')) == 4):
        return False,'按年统计时间范围有误!'
    if params.get('time_kind') == 'day' and (
        not len(params.get('start_time')) == 10 or not len(params.get('end_time')) == 10):
        return False,'按日统计时间范围有误!'
    return True,'success'

#时间增长 几天几个月几年
def date_up(begin,several):
    if several == 0:
        return begin
    several = several - 1
    if len(begin) == 4:
        return int(begin) + several
    elif len(begin) == 7:
        b = begin.split('-')
        m = int(b[1]) + several
        y = int(b[0])
        if m > 12:
            y = int(b[0]) + int(m / 12)
            m = m % 12
        result_date = str(y) + '-' + str(m)
        return result_date
    else:
        b = begin.split('-')
        s = datetime.date(int(b[0]), int(b[1]), int(b[2]))
        result_date = s + datetime.timedelta(days=several)
        return result_date.strftime('%Y-%m-%d')

#判断哪个时间大
def mix_min_check(start,end):
    a = int(start.replace('-',''))
    b = int(end.replace('-', ''))
    if a>b:
        return False
    return True
