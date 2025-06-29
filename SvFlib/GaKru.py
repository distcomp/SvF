# -*- coding: cp1251 -*-
from __future__ import division
#from   numpy         import *
import numpy as np
#from   pyomo.environ import *
import COMMON        as     co




Pi  = np.pi #' Число Пи
#Pi  = 3.14159265358979 #' Число Пи
ro  = 206264.8062 #' Число угловых секунд в радиане

#' Эллипсоид Красовского
aP  = 6378245               #' Большая полуось
alP  = 1 / 298.3            # ' Сжатие
e2P  = 2 * alP - alP ** 2   # Квадрат эксцентриситета

#' Эллипсоид WGS84 (GRS80, эти два эллипсоида сходны по большинству параметров)
aW  = 6378137                   # Большая полуось
alW  = 1 / 298.257223563        # Сжатие
e2W  = 2 * alW - alW ** 2       # Квадрат эксцентриситета

#' Вспомогательные значения для преобразования эллипсоидов
a  = (aP + aW) / 2
e2  = (e2P + e2W) / 2
da  = aW - aP
de2  = e2W - e2P

#' Линейные элементы трансформирования, в метрах
dx  = 23.92
dy  = -141.27
dz  = -80.9

#' Угловые элементы трансформирования, в секундах
wx  = 0
wy  = 0
wz  = 0

#' Дифференциальное различие масштабов
ms  = 0


def dB( Bd, Ld, H) :
    B = Bd * Pi / 180;
    L = Ld * Pi / 180;
    M = a * (1 - e2) / pow((1 - e2 * pow(np.sin(B) , 2)) , 1.5);
    N = a * pow((1 - e2 * pow(np.sin(B) , 2)) , -0.5);
    return ro / (M + H) * (N / a * e2 * np.sin(B) * np.cos(B) * da + ((N * N) / (a * a) + 1) * N * np.sin(B) * np.np.cos(B) * de2 / 2 - (dx * np.np.cos(L) + dy * np.sin(L)) * np.sin(B) + dz * np.np.cos(B)) - wx * np.sin(L) * (1 + e2 * np.np.cos(2 * B)) + wy * np.np.cos(L) * (1 + e2 * np.np.cos(2 * B)) - ro * ms * e2 * np.sin(B) * np.np.cos(B);


def dL( Bd, Ld, H) :
    B = Bd * Pi / 180;
    L = Ld * Pi / 180;
    N = a * pow((1 - e2 * pow(np.sin(B) , 2)) , -0.5);
    return ro / ((N + H) * np.np.cos(B)) * (-dx * np.sin(L) + dy * np.np.cos(L)) + tan(B) * (1 - e2) * (wx * np.np.cos(L) + wy * np.sin(L)) - wz;

def WGS84Alt( Bd, Ld, H) :
    B = Bd * Pi / 180;
    L = Ld * Pi / 180;
    N = a * pow((1 - e2 * pow(np.sin(B) , 2)) , -0.5);
    dH = -a / N * da + N * pow(np.sin(B) , 2) * de2 / 2 + (dx * np.np.cos(L) + dy * np.sin(L)) * np.np.cos(B) + dz * np.sin(B) - N * e2 * np.sin(B) * np.np.cos(B) * (wx / ro * np.sin(L) - wy / ro * np.np.cos(L)) + ((a * a) / N + H) * ms;
    return H + dH;

###################  градусы в градусы  ############################

def WGS84_SK42_Lat( Bd, Ld, H) :
    return Bd - dB(Bd, Ld, H) / 3600;

def SK42_WGS84_Lat( Bd, Ld, H) :
    return Bd + dB(Bd, Ld, H) / 3600;

def WGS84_SK42_Long( Bd, Ld, H) :
    return Ld - dL(Bd, Ld, H) / 3600;

def SK42_WGS84_Long( Bd, Ld, H) :
    return Ld + dL(Bd, Ld, H) / 3600;

def SK42toWGS84( Bd, Ld, H) :
    return SK42_WGS84_Lat( Bd, Ld, H), SK42_WGS84_Long( Bd, Ld, H)

def WGS84toSK42( Bd, Ld, H) :
    return WGS84_SK42_Lat( Bd, Ld, H), WGS84_SK42_Long( Bd, Ld, H)

####################################################################

## Функции преобразования в координатную проекцию Гаусса-Крюгера
#  град в м
def SK42BTOX( B, L, H) :
    No = int((6 + L) / 6. )
    Lo = (L - (3 + 6 * (No - 1))) / 57.29577951;
    Bo = B * Pi / 180;
    Xa = pow(Lo , 2) * (109500 - 574700 * pow(np.sin(Bo) , 2) + 863700 * pow(np.sin(Bo) , 4) - 398600 * pow(np.sin(Bo) , 6));
    Xb = pow(Lo , 2) * (278194 - 830174 * pow(np.sin(Bo) , 2) + 572434 * pow(np.sin(Bo) , 4) - 16010 * pow(np.sin(Bo) , 6) + Xa);
    Xc = pow(Lo , 2) * (672483.4 - 811219.9 * pow(np.sin(Bo) , 2) + 5420 * pow(np.sin(Bo) , 4) - 10.6 * pow(np.sin(Bo) , 6) + Xb);
    Xd = pow(Lo , 2) * (1594561.25 + 5336.535 * pow(np.sin(Bo) , 2) + 26.79 * pow(np.sin(Bo) , 4) + 0.149 * pow(np.sin(Bo) , 6) + Xc);
    return 6367558.4968 * Bo - np.sin(Bo * 2) * (16002.89 + 66.9607 * pow(np.sin(Bo) , 2) + 0.3515 * pow(np.sin(Bo) , 4) - Xd);

def SK42LTOY( B, L, H) :   #lat, long
    No = int((6 + L) / 6. )
    Lo = (L - (3 + 6 * (No - 1))) / 57.29577951;
    Bo = B * Pi / 180;
    Ya = pow(Lo , 2) * (79690 - 866190 * pow(np.sin(Bo) , 2) + 1730360 * pow(np.sin(Bo) , 4) - 945460 * pow(np.sin(Bo) , 6));
    Yb = pow(Lo , 2) * (270806 - 1523417 * pow(np.sin(Bo) , 2) + 1327645 * pow(np.sin(Bo) , 4) - 21701 * pow(np.sin(Bo) , 6) + Ya);
    Yc = pow(Lo , 2) * (1070204.16 - 2136826.66 * pow(np.sin(Bo) , 2) + 17.98 * pow(np.sin(Bo) , 4) - 11.99 * pow(np.sin(Bo) , 6) + Yb);
    return (5 + 10 * No) * 100000 + Lo * np.np.cos(Bo) * (6378245 + 21346.1415 * pow(np.sin(Bo) , 2) + 107.159 * pow(np.sin(Bo) , 4) + 0.5977 * pow(np.sin(Bo) , 6) + Yc);

def SK42toGausKru( B42, L42, H) :   # lat, lon
    return SK42LTOY( B42, L42, H), SK42BTOX(B42, L42, H)

def WGS84toGausKru( B84, L84, H) :   # lat, lon
    Lat42, Lon42 = WGS84toSK42( B84, L84, 0)
    return SK42LTOY( Lat42, Lon42, H), SK42BTOX( Lat42, Lon42, H )   # x, y


def ListLBWGS84toGausKru( LB ) :   # [lon, lat]
    ret = []
    for p in range(0,len(LB),2) :
        x, y = WGS84toGausKru( LB[1+p], LB[0+p], 0)
        ret.append(x)
        ret.append(y)
    return ret


#   м в град


def SK42XTOB(X, Y, Z) :
    No = Y * 10 ** -6
    No = int(No)
    Bi = X / 6367558.4968
    Bo = Bi + np.sin(Bi * 2) * (0.00252588685 - 0.0000149186 * np.sin(Bi) ** 2 + 0.00000011904 * np.sin(Bi) ** 4)
    Zo = (Y - (10 * No + 5) * 10 ** 5) / (6378245 * np.np.cos(Bo))
    Ba = Zo ** 2 * (0.01672 - 0.0063 * np.sin(Bo) ** 2 + 0.01188 * np.sin(Bo) ** 4 - 0.00328 * np.sin(Bo) ** 6)
    Bb = Zo ** 2 * (0.042858 - 0.025318 * np.sin(Bo) ** 2 + 0.014346 * np.sin(Bo) ** 4 - 0.001264 * np.sin(Bo) ** 6 - Ba)
    Bc = Zo ** 2 * (0.10500614 - 0.04559916 * np.sin(Bo) ** 2 + 0.00228901 * np.sin(Bo) ** 4 - 0.00002987 * np.sin(Bo) ** 6 - Bb)
    dB = Zo ** 2 * np.sin(Bo * 2) * (0.251684631 - 0.003369263 * np.sin(Bo) ** 2 + 0.000011276 * np.sin(Bo) ** 4 - Bc)
    return  (Bo - dB) * 180 / Pi






def SK42YTOL(X, Y, Z) :
     No = Y * 10 ** -6
     No = int(No)
     Bi = X / 6367558.4968
     Bo = Bi + np.sin(Bi * 2) * (0.00252588685 - 0.0000149186 * np.sin(Bi) ** 2 + 0.00000011904 * np.sin(Bi) ** 4)
     Zo = (Y - (10 * No + 5) * 10 ** 5) / (6378245 * np.np.cos(Bo))
     La = Zo ** 2 * (0.0038 + 0.0524 * np.sin(Bo) ** 2 + 0.0482 * np.sin(Bo) ** 4 + 0.0032 * np.sin(Bo) ** 6)
     Lb = Zo ** 2 * (0.01225 + 0.09477 * np.sin(Bo) ** 2 + 0.03282 * np.sin(Bo) ** 4 - 0.00034 * np.sin(Bo) ** 6 - La)
     Lc = Zo ** 2 * (0.0420025 + 0.1487407 * np.sin(Bo) ** 2 + 0.005942 * np.sin(Bo) ** 4 - 0.000015 * np.sin(Bo) ** 6 - Lb)
     Ld = Zo ** 2 * (0.16778975 + 0.16273586 * np.sin(Bo) ** 2 - 0.0005249 * np.sin(Bo) ** 4 - 0.00000846 * np.sin(Bo) ** 6 - Lc)
     dL = Zo * (1 - 0.0033467108 * np.sin(Bo) ** 2 - 0.0000056002 * np.sin(Bo) ** 4 - 0.0000000187 * np.sin(Bo) ** 6 - Ld)
     return  (6 * (No - 0.5) / 57.29577951 + dL) * 180 / Pi




def GausKruToSK42( X, Y, Z) :
    return SK42XTOB( Y, X, Z), SK42YTOL( Y, X, Z)   # lat, lon   x, y - пришлось поменять местами

def GausKruToWGS84( X, Y, Z ) :   # x, y
    B42, L42 = GausKruToSK42(X, Y, Z)
    return SK42toWGS84(B42, L42, Z)   # lat, lon

##########         AZIMUT             #######################################

RADpGRAD = Pi/180
EARTH =  6400.

def AzimutInit ( cen_lat_grad, cen_lon_grad ) :     # B,  L
        co.lon_center_rad = cen_lon_grad * RADpGRAD
        co.lat_center_rad = cen_lat_grad * RADpGRAD
        co.sin_lat_center_rad = np.sin ( co.lat_center_rad )
        co.cos_lat_center_rad = np.cos ( co.lat_center_rad )


def LatLonToAzimut_scalar ( lat_grad, lon_grad ) :     # B,  L
          lo = lon_grad * RADpGRAD
          la = lat_grad * RADpGRAD
          sin_la = np.sin ( la )
          cos_la = np.cos ( la )
          loMlon_center_rad = lo-co.lon_center_rad
          cos_loMlon_center_rad = np.cos(loMlon_center_rad)
          Z = sin_la * co.sin_lat_center_rad + cos_la * co.cos_lat_center_rad * cos_loMlon_center_rad
          if  Z < 0 :
              km_x = None 
              km_y = None
          else :    
              km_x = cos_la * np.sin(loMlon_center_rad) * EARTH
              km_y = EARTH * (sin_la * co.cos_lat_center_rad - cos_la * co.sin_lat_center_rad * cos_loMlon_center_rad )
          return km_x, km_y


def AzimutToLatLon ( km_x, km_y ):  # B,  L  return lat_grad, lon_grad
        Xkm = km_x / EARTH
        Ykm = km_y / EARTH
        Z = 1. - Xkm*Xkm - Ykm*Ykm
        if ( Z < 0 ) :  return  None, None

        Z = np.sqrt ( Z )
        sin_lat = np.sin ( co.lat_center_rad )
        np.cos_lat = np.np.cos ( co.lat_center_rad )
        ar = Z * sin_lat + Ykm * np.cos_lat
        if ( ar >  1. ): ar =  1
        if ( ar < -1. ):  ar = -1
        mat_y  = asin ( ar )

        np.cos_la = np.cos ( mat_y  )
        if ( fabs ( np.cos_la ) < 1.0e-20 ) : ar = 1;
        else 				             : ar = Xkm / np.cos_la;
        if ( ar >  1 ) : ar =  1;
        if ( ar < -1 ) : ar = -1;
        if((Z-np.sin(mat_y)*sin_lat)*np.cos_la*np.cos_lat<0.):
            mat_x = 180+(co.lon_center_rad-asin(ar))/RADpGRAD
        else :
            mat_x =     (co.lon_center_rad+asin(ar))/RADpGRAD
        mat_y /= RADpGRAD

        if ( mat_x <    0. ): mat_x += 360
        if ( mat_x >  360. ): mat_x -= 360
        if ( mat_x < -180. ): mat_x += 360
        if ( mat_x >  180. ): mat_x -= 360

#        print (mat_x, mat_y)
        return  mat_y, mat_x        # lat_grad, lon_grad



def  arrayLatLonToAzimut(lat, lon, x, y) :
        for i in range(x.shape[0]):  x[i],y[i] = LatLonToAzimut( float(lat[i]),float(lon[i]) )

def  arrayAzimutToLatLon (lat, lon, x, y) :
        for i in range(lat.shape[0]):  lat[i], lon[i]  = AzimutToLatLon(x[i], y[i])

def LatLonToAzimut ( lat_grad, lon_grad ) :     # B,  L     для чисел и МАССИВОВ
 #       print ('type(lat_grad)', type(lat_grad))
        if type(lat_grad) == type(1.0):
            return LatLonToAzimut_scalar(lat_grad, lon_grad)
        else:
            NoR = len(lat_grad)
#            print ('lat_grad****', NoR)
            x = np.zeros(NoR, np.float64)
            y = np.zeros(NoR, np.float64)
            for i in range (NoR) :
                x[i],y[i] = LatLonToAzimut_scalar ( lat_grad[i], lon_grad[i] )
            return x,y

##### !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! ##################### попытка
from pyproj import Proj, transform

# Определим систему координат WGS84 (широта и долгота)
wgs84 = Proj(proj='latlong', datum='WGS84')

# Определим систему координат Гаусса-Крюгера (например, зону 3 для России)
#gauss_kruger = Proj(proj='tmerc', lat_0=0, lon_0=9, k=1, x_0=500000, y_0=0, ellps='krass', units='m')
gauss_kruger_zone_5 = Proj(proj='tmerc', lat_0=0, lon_0=33, k=1, x_0=500000, y_0=0, ellps='krass', units='m')
gauss_kruger_zone_5abc = Proj(proj='tmerc', lat_0=0, lon_0=33, k=1, x_0=6500000, y_0=0, ellps='krass', units='m')

# Пример координат в системе WGS84 (широта и долгота)
#latitude = 55.7558  # Москва
#longitude = 37.6173
latitudeAAA = 53.2521  # Брянск
longitudeAAA = 34.3717

# Преобразование координат из WGS84 в проекцию Гаусса-Крюгера
#x, y = transform(wgs84, gauss_kruger, longitude, latitude)
xAAA, yAAA = transform(wgs84, gauss_kruger_zone_5abc, longitudeAAA, latitudeAAA)

#print(f'Координаты в системе Гаусса-Крюгера: X={x}, Y={y}')
#x,y = WGS84toGausKru( latitude,longitude, 0)
#print ('JJJJJJJJJJJJJJJJJJ', xAAA,yAAA)
#1/0
