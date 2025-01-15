import datetime
import earth
from math import pi, sin, cos

def datetime_to_julian_date(dt):
    # 修正月份和年份
    year = dt.year
    month = dt.month
    day = dt.day
    hour = dt.hour
    minute = dt.minute
    second = dt.second
    
    if month <= 2:
        year -= 1
        month += 12
    
    # 计算 A 和 B
    A = int(year / 100)
    B = 2 - A + int(A / 4)
    
    # 计算儒略日
    JD = int(365.25 * (year + 4716)) + int(30.6001 * (month + 1)) + day + B - 1524.5
    JD += (hour - 12) / 24 + minute / 1440 + second / 86400
    
    return JD

def julian_date_to_gmst(jd):
    # 基准时刻 J2000.0 对应的儒略日
    jd_j2000 = datetime.datetime(2000, 1, 1, 12, 0, 0)
    
    # 计算 T，以儒略世纪为单位
    T = (datetime_to_julian_date(jd) - datetime_to_julian_date(jd_j2000)) / 36525.0
    print(T)
    
    # 计算 GMST，单位为小时
    gmst_hours = (18.697374558 + 24.06570982441908 * T + 1.00273790935 * (datetime_to_julian_date(jd) - datetime_to_julian_date(jd_j2000)) + 0.000026 * T**2 + 0.0000000278 * T**3) % 24
    
    print(gmst_hours)
    print("22222")
    # 将 GMST 转换为度
    gmst_rad = gmst_hours * 15 * pi / 180
    
    return gmst_rad

t_dt = datetime.datetime(2025, 1, 9, 10, 32, 29)
# print(earth.getGmst(t_dt))
print(julian_date_to_gmst(t_dt))
# rSiteLla_radm = [39.96 * pi / 180, 116.32 * pi / 180, 0]
rSiteLla_radm = [39.96, 116.32, 0]
# rSiteLla_radm = [116.32, 39.96, 0]
rSiteEci_m = earth.lla2eci(rSiteLla_radm, t_dt)
print(rSiteEci_m)