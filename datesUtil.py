#!/usr/bin/python
# coding=utf-8
# 时间计算工具类
import datetime
import calendar

# 根据配置年月日星期获取时间数组
def getDates(data):
    times = []
    # 如果所有参数都为空，返回空数组
    if not data.get("years") and not data.get("months") and not data.get("dates") and not data.get("days"):
        return []
    years = []
    months = []
    dates = []
    days = []
    current = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    current_year = current[0:4]
    current_month = current[5:7]
    current_date = current[8:10]
    current_day = str(datetime.datetime.now().weekday()+1)

    # 如果年为空，取当前年
    if not data.get("years"):
        years.append(current_year)
    else:
        years = data.get("years")
    # 如果月为空，取当前月
    if not data.get("months"):
        months.append(current_month)
    else:
        months = data.get("months")

    dates = data.get("dates")
    days = data.get("days")
    # # 如果日为空,星期也为空，取当前日
    # if not data.get("dates") and not data.get("days"):
    #     dates.append(current_date)
    # else:
    #     dates = data.get("dates")
    # # 如果星期为空，取当前星期
    # if not data.get("days"):
    #     days.append(current_day)
    # else:
    #     days = data.get("days")

    # 配置年月日
    for year in years:
        for month in months:
            if dates:
                for date in dates:
                    times.append(year+"-"+month+"-"+date)
            else:
                # 获取month月天数
                date_count = calendar.monthrange(int(year), int(month))[1]
                date = 1
                while date <= date_count:
                    times.append(year + "-" + month + "-" + (str(date) if date >= 10 else "0" + str(date)))
                date += 1
    # 配置星期几,获取配置的年月份里与配置星期几对应的日期
    for year in years:
        for month in months:
            # 获取month月天数
            date_count = calendar.monthrange(int(year),int(month))[1]
            date = 1
            while date <= date_count:
                weekday = calendar.weekday(int(year),int(month),int(date)) + 1
                for day in days:
                    if int(weekday) == int(day):
                        times.append(year+"-"+month+"-"+(str(date) if date >=10 else "0"+str(date)))
                date += 1

    return times

if __name__ == '__main__':
    print(getDates({"days":[2,4,6]}))
    marketProfit = 1
    if marketProfit:
        print("66666666666")