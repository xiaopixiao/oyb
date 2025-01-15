import datetime
import earth
from math import pi, sin, cos

t_dt = datetime.datetime(2016, 11, 2, 5, 39, 5)
rSiteLla_radm = [40 * pi / 180, 116 * pi / 180, 0]
rSiteEci_m = earth.lla2eci(rSiteLla_radm, t_dt)
print(rSiteEci_m)