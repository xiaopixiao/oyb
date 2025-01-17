import datetime
import earth
from math import pi, sin, cos
from sgp4.api import Satrec, WGS72, jday
from sgp4 import exporter
import numpy as np

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

# t_dt = datetime.datetime(2025, 1, 9, 8, 39, 34)
# t_dt2 = datetime.datetime(2025, 1, 9, 8, 39, 34, 500)
# t_dt3 = datetime.datetime(2025, 1, 9, 8, 39, 33, 500)
# jd, fr = jday(2025, 1, 9, 8, 39, 34)
t_dt = datetime.datetime(2025, 1, 9, 8, 43, 34)
t_dt2 = datetime.datetime(2025, 1, 9, 8, 43, 35)
t_dt3 = datetime.datetime(2025, 1, 9, 8, 43, 33)
jd, fr = jday(2025, 1, 9, 8, 43, 34)
# print(earth.getGmst(t_dt))
print(julian_date_to_gmst(t_dt))
rSiteLla_radm = [39.96 * pi / 180, 116.32 * pi / 180, 0]
# rSiteLla_radm = [39.96, 116.32, 0]
# rSiteLla_radm = [116.32, 39.96, 0]
rSiteEci_m = earth.lla2eci(rSiteLla_radm, t_dt)
rSiteEci_m2 = earth.lla2eci(rSiteLla_radm, t_dt2)
rSiteEci_m3 = earth.lla2eci(rSiteLla_radm, t_dt3)
print(rSiteEci_m)
print(rSiteEci_m2)
print(rSiteEci_m3)
vSiteEci_m = (rSiteEci_m2 - rSiteEci_m3) / 2
print(vSiteEci_m)

s = '1 57288U 23095A   24346.12889920  .00000102  00000-0  16104-3 0  9995'
t = '2 57288  86.5052 196.1410 0016507 293.2760  66.6644 13.39495368 69714'

# s = '1 00900U 64063C   25005.62601295  .00001399  00000+0  14355-2 0  9992'
# t = '2 00900  90.2094  59.7713 0027525  91.1587  79.5004 13.75727213998851'

# 初始化Satrec对象
satellite = Satrec.twoline2rv(s, t)

# 设置日期和时间
# now = datetime(2024, 12, 11, 4, 0, 0)
# epoch_sec = (now - datetime(2006, 1, 1, 12, 0, 0)).total_seconds()
#


print(jd)
print(fr)

# 计算卫星位置和速度
e, position, velocity = satellite.sgp4(jd, fr)
print("e:", e)
print("Position:", position)
print("Velocity:", velocity)
rSate = np.array(position) * 1000
vSate = np.array(velocity) * 1000
# vc = np.dot(rSate - rSiteEci_m, vSate - vSiteEci_m) / np.linalg.norm(rSate - rSiteEci_m)
# vc = np.dot(rSiteEci_m - rSate, vSiteEci_m - vSate) / np.linalg.norm(rSiteEci_m - rSate)
vc = np.dot(vSiteEci_m - vSate, rSiteEci_m - rSate) / np.linalg.norm(rSiteEci_m - rSate)
deltaf = - vc / 299792458 * 1.6e9
print(deltaf)
aaa = []

for i in range(38, 52):
    s = '1 57288U 23095A   24346.12889920  .00000102  00000-0  16104-3 0  9995'
    t = '2 57288  86.5052 196.1410 0016507 293.2760  66.6644 13.39495368 69714'

    # s = '1 00900U 64063C   25005.62601295  .00001399  00000+0  14355-2 0  9992'
    # t = '2 00900  90.2094  59.7713 0027525  91.1587  79.5004 13.75727213998851'

    # 初始化Satrec对象
    satellite = Satrec.twoline2rv(s, t)

    # 设置日期和时间
    # now = datetime(2024, 12, 11, 4, 0, 0)
    # epoch_sec = (now - datetime(2006, 1, 1, 12, 0, 0)).total_seconds()
    #
    t_dt = datetime.datetime(2025, 1, 9, 8, i, 34)
    t_dt2 = datetime.datetime(2025, 1, 9, 8, i, 35)
    t_dt3 = datetime.datetime(2025, 1, 9, 8, i, 33)
    jd, fr = jday(2025, 1, 9, 8, i, 34)

    rSiteEci_m = earth.lla2eci(rSiteLla_radm, t_dt)
    rSiteEci_m2 = earth.lla2eci(rSiteLla_radm, t_dt2)
    rSiteEci_m3 = earth.lla2eci(rSiteLla_radm, t_dt3)

    vSiteEci_m = (rSiteEci_m2 - rSiteEci_m3) / 2


    # 计算卫星位置和速度
    e, position, velocity = satellite.sgp4(jd, fr)
    print("e:", e)
    print("Position:", position)
    print("Velocity:", velocity)
    rSate = np.array(position) * 1000
    vSate = np.array(velocity) * 1000
    # vc = np.dot(rSate - rSiteEci_m, vSate - vSiteEci_m) / np.linalg.norm(rSate - rSiteEci_m)
    # vc = np.dot(rSiteEci_m - rSate, vSiteEci_m - vSate) / np.linalg.norm(rSiteEci_m - rSate)
    vc = np.dot(vSiteEci_m - vSate, rSiteEci_m - rSate) / np.linalg.norm(rSiteEci_m - rSate)
    deltaf = - vc / 299792458 * 1.6e9
    aaa.append(deltaf)

print(aaa)