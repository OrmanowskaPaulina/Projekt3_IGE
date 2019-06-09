# -*- coding: utf-8 -*-
"""
Created on Tue May 28 13:09:44 2019
    
@author: paula
"""
from math import sin, tan, atan, cos, sqrt,  radians
import gpxpy
from datetime import timedelta
    
def vincent(fi_aa,la_aa,fi_bb,la_bb): #algorytm vincentego
    
    if fi_aa == fi_bb and la_aa == la_bb:
        s_AB = 0
    else:
        fi_a = radians(fi_aa)
        fi_b = radians(fi_bb)
        la_a = radians(la_aa)
        la_b = radians(la_bb)
        
        a = 6378137.000;
        e2 = 0.00669438002290;
    
        b = a*sqrt(1-e2);
        f = 1 - (b/a);
        
        delta_la = la_b - la_a
        U_a = atan((1-f)*tan(fi_a))
        U_b = atan((1-f)*tan(fi_b))
        L = delta_la;
    
        
        while True:
            sin_sigma = sqrt((cos(U_b)*sin(L))**2 + (cos(U_a)*sin(U_b) - sin(U_a)*cos(U_b)*cos(L))**2);
            cos_sigma = sin(U_a)*sin(U_b) + cos(U_a)*cos(U_b)*cos(L);
            sigma = atan(sin_sigma/cos_sigma);
            sin_alfa = (cos(U_a)*cos(U_b)*sin(L))/(sin_sigma); 
            cos2_alfa = 1 - (sin_alfa)**2;
            cos2_sigma_m = cos_sigma - (2*sin(U_a)*sin(U_b))/(cos2_alfa);
            C = (f/16)*cos2_alfa*(4+f*(4-3*cos2_alfa));
            Ls = L;
            L = delta_la + (1-C)*f*sin_alfa*(sigma + C*sin_sigma*(cos2_sigma_m + C*cos_sigma*(-1+2*(cos2_sigma_m)**2)));
            if (L-Ls)<(0.000001/206265):
                break
        
        
        u2 = ((a**2 - b**2)/b**2)*cos2_alfa
        A = 1 + (u2/16384)*(4096 + u2*(-768 + u2*(320 - 175*u2)))
        B = (u2/1024)*(256 + u2*(-128 + u2*(74 - 47*u2)))
        delta_sigma = B*sin_sigma*(cos2_sigma_m + (1/4)*B*(cos_sigma*(-1 + 2*(cos2_sigma_m)**2) - (1/6)*B*cos2_sigma_m*(-3 + 4*(sin_sigma)**2)*(-3 + 4*(cos2_sigma_m)**2)));
        s_AB = b*A*(sigma - delta_sigma)
    
    return s_AB
    
    
def wczytaj_dane(filename):
    lat = []
    lon = []

    with open(filename, 'r') as gpx_file:
        gpx_dane = gpxpy.parse(gpx_file)
    
    for track in gpx_dane.tracks:
        for seg in track.segments:
            for point in seg.points:
                lon.append(point.longitude)
                lat.append(point.latitude)

    return lat, lon

def statystyki(filename):
    lat = []
    lon = []
    el = []
    dates = []

    with open(filename, 'r') as gpx_file: 
        gpx_dane = gpxpy.parse(gpx_file)
    
    for track in gpx_dane.tracks:
        for seg in track.segments:
            for point in seg.points:
                lon.append(point.longitude)
                lat.append(point.latitude)
                el.append(point.elevation)
                point.time = point.time.replace(tzinfo=None)
                dates.append(point.time)
                    
    dh = []  
    dhg = []
    dhd = []
          
    w = len(el)
    for i in range(len(el)):
        if i + 1 >= w:
            break
        else:
            x = el[i+1] - el[i]
            dh.append(x)
            if x > 0:
                dhg.append(x)
            else:
                dhd.append(x)
                

    dh_g = sum(dhg)
    dh_d = sum(dhd)        
    DH = sum(dh)

       
    odl = []
    suma_odl = 0
    odl2 = []
    for i in range(len(lon)):
        if i + 1 >= len(lon):
            break
        else:       
            s = vincent(lat[i], lon[i], lat[i+1], lon[i+1])
            suma_odl += s   
            odl2d = s
            odl2.append(odl2d)
            odl.append(suma_odl) 
            
    
    
    czas = []
    suma_t = 0
    for t in range(len(dates)):
        if t + 1 >= len(dates):
            break
        else:
            dt = dates[t+1] - dates[t]
            dt2 = dt.total_seconds()
            suma_t += dt2
            czas.append(suma_t)
    czas_ost = timedelta(seconds=suma_t)
    
    
    v = (suma_odl/suma_t)*3.6  #km/h 

    staty = "Odległosc: {} km\nCzas: {}\nSrednia prędkosc: {} km/h\nPrzewyzszenie calkowite: {}m\nPrzewyzszenie w gore: {}m\nPrzewyzszenie w dol: {}m".format(round(suma_odl/1000, 3), czas_ost, round(v,2), round(DH,3), round(dh_g,3), round(dh_d,3))         
             

    return el, dates, DH, suma_odl, odl, czas_ost, czas, v, staty