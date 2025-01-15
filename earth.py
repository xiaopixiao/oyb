"""Defines earth parameters and key earth-specific calculations (ECF/ENU frame
   conversions, latitude/longitude, GMST, etc.).
"""

from __future__ import division
import numpy
import datetime
from math import pi, sin, cos, radians, sqrt
import rot

# Key Earth parameters
mu_m3ps2 = 3.986e14
tSidDay_s = 23 * 3600 + 56 * 60 + 4.0916
# eqRad_m = 6.3781e6
eqRad_m = 6.371393e6
j2000_dt = datetime.datetime(2000, 1, 1, 12, 0, 0)
flatness = 0.003353
# flatness = 0.00335
j2 = 1.08263e-3
tSidYear_s = 365.25636 * 86400

def getGmst(t_dt):
    """Returns GMST--the angle (in radians) between the first point of Aries
       and 0-longitude--at the given *datetime.datetime* value.
    """
    dt_days = (t_dt - j2000_dt).total_seconds() / 86400
    gmst_hrs = 18.697374558 + 24.06570982441908 * dt_days
   #  gmst_hrs = 18.697374558 + 24.0657047 * dt_days + 1.00273790935 * 0.000026 * dt_days ** 2 + 0.0000000278 * dt_days ** 3
   #  gmst_hrs = 18.697374558 + 24.0 * dt_days
    print(gmst_hrs)
    print("11111")
    print(2 * pi * (gmst_hrs % 24) / 24)
    return 2 * pi * (gmst_hrs % 24) / 24

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

    Du = datetime_to_julian_date(jd) - datetime_to_julian_date(jd_j2000)
    
    # 计算 T，以儒略世纪为单位
    T = Du / 36525.0
    print(T)
    
    # 计算 GMST，单位为小时
   #  gmst_hours = (18.697374558 + 24.06570982441908 * T + 1.00273790935 * (datetime_to_julian_date(jd) - datetime_to_julian_date(jd_j2000)) + 0.000026 * T**2 + 0.0000000278 * T**3) % 24
    
    gmst_rad = 2 * pi * (0.7790572732640 + 1.00273781191135448 * Du) + (0.014506 + 4612.15739966 * T + 1.39667721 * T**2 - 0.00009344 * T**3 + 0.00001882 * T**4) * (pi / 180) / 3600

   #  print(gmst_hours)
    print(gmst_rad)
    print("22222")
    # 将 GMST 转换为度
   #  gmst_rad = gmst_hours * 15 * pi / 180
    
    return gmst_rad

def lla_to_ecef(lat, lon, alt):
    # WGS-84 参数
    a = 6378137.0  # 半长轴
    e2 = 0.00669437999014  # 第一偏心率平方
    
    # 将经纬度转换为弧度
    lat_rad = radians(lat)
    lon_rad = radians(lon)
    
    # 计算 N
    N = a / sqrt(1 - e2 * sin(lat_rad) ** 2)
    
    # 计算 ECEF 坐标
    X = (N + alt) * cos(lat_rad) * cos(lon_rad)
    Y = (N + alt) * cos(lat_rad) * sin(lon_rad)
    Z = (N * (1 - e2) + alt) * sin(lat_rad)
    
    return X, Y, Z

def ecef_to_eci(X, Y, Z, gmst):
    # 构建旋转矩阵
    R = [
        [cos(gmst), sin(gmst), 0],
        [-sin(gmst), cos(gmst), 0],
        [0, 0, 1]
    ]
    
    # 计算 ECI 坐标
    X_eci = R[0][0] * X + R[0][1] * Y + R[0][2] * Z
    Y_eci = R[1][0] * X + R[1][1] * Y + R[1][2] * Z
    Z_eci = R[2][0] * X + R[2][1] * Y + R[2][2] * Z
    
    return X_eci, Y_eci, Z_eci

def lla2eci(rLla_radm, t_dt):
    """Computes the geocentric inertial position of the site at the given
       lat/lon/altitude, using a spheroid earth and a specific datetime.
    """
    ra_rad = rLla_radm[1] + getGmst(t_dt)
    ra_rad = rLla_radm[1] + julian_date_to_gmst(t_dt)
    gmst = julian_date_to_gmst(t_dt)
   #  gmst = getGmst(t_dt)
    x_ecef, y_ecef, z_ecef = lla_to_ecef(rLla_radm[0], rLla_radm[1], rLla_radm[2])
    x, y, z = ecef_to_eci(x_ecef, y_ecef, z_ecef, gmst)

   #  d = (1 - (2 * flatness - flatness**2) * sin(rLla_radm[0])**2)**0.5
   #  x = (eqRad_m / d + rLla_radm[2]) * cos(rLla_radm[0]) * cos(ra_rad)
   #  y = (eqRad_m / d + rLla_radm[2]) * cos(rLla_radm[0]) * sin(ra_rad)
   #  z = (eqRad_m * (1 - flatness)**2 / d + rLla_radm[2]) * sin(rLla_radm[0])
    return numpy.array([x,y,z])
    
def getQeci2ecf(t_dt):
    """Returns a 3x3 numpy.array that defines a transformation (at this level of
       fidelity, just a Z rotation) from the ECI to ECF frame at the given
       *datetime.datetime* value.
    """
    return rot.Z(getGmst(t_dt))

def getQecf2enu(rSiteLla_radm):
    """Returns a transformation matrix that converts an ECF vector to ENZ as
       perceived from a site at the given lat/lon/alt location. Note that this
       is a frame rotation only--relative range requires user subtraction.
    """
    Quen2enu = numpy.array([[0,1,0], [0,0,1], [1,0,0]])
    ry = rot.Y(-rSiteLla_radm[0])
    rz = rot.Z(rSiteLla_radm[1])
    return Quen2enu.dot(ry).dot(rz)

def getRotVel():
    """Returns the rotational velocity of the earth, in radians per second.
    """
    return 2 * pi / tSidDay_s
