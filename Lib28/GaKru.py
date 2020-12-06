# -*- coding: cp1251 -*-
from __future__ import division
from   numpy         import *
from   pyomo.environ import *
import COMMON        as     co



Pi  = pi #' Число Пи
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
    M = a * (1 - e2) / pow((1 - e2 * pow(sin(B) , 2)) , 1.5);
    N = a * pow((1 - e2 * pow(sin(B) , 2)) , -0.5);
    return ro / (M + H) * (N / a * e2 * sin(B) * cos(B) * da + ((N * N) / (a * a) + 1) * N * sin(B) * cos(B) * de2 / 2 - (dx * cos(L) + dy * sin(L)) * sin(B) + dz * cos(B)) - wx * sin(L) * (1 + e2 * cos(2 * B)) + wy * cos(L) * (1 + e2 * cos(2 * B)) - ro * ms * e2 * sin(B) * cos(B);


def dL( Bd, Ld, H) :
    B = Bd * Pi / 180;
    L = Ld * Pi / 180;
    N = a * pow((1 - e2 * pow(sin(B) , 2)) , -0.5);
    return ro / ((N + H) * cos(B)) * (-dx * sin(L) + dy * cos(L)) + tan(B) * (1 - e2) * (wx * cos(L) + wy * sin(L)) - wz;

def WGS84Alt( Bd, Ld, H) :
    B = Bd * Pi / 180;
    L = Ld * Pi / 180;
    N = a * pow((1 - e2 * pow(sin(B) , 2)) , -0.5);
    dH = -a / N * da + N * pow(sin(B) , 2) * de2 / 2 + (dx * cos(L) + dy * sin(L)) * cos(B) + dz * sin(B) - N * e2 * sin(B) * cos(B) * (wx / ro * sin(L) - wy / ro * cos(L)) + ((a * a) / N + H) * ms;
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
    Xa = pow(Lo , 2) * (109500 - 574700 * pow(sin(Bo) , 2) + 863700 * pow(sin(Bo) , 4) - 398600 * pow(sin(Bo) , 6));
    Xb = pow(Lo , 2) * (278194 - 830174 * pow(sin(Bo) , 2) + 572434 * pow(sin(Bo) , 4) - 16010 * pow(sin(Bo) , 6) + Xa);
    Xc = pow(Lo , 2) * (672483.4 - 811219.9 * pow(sin(Bo) , 2) + 5420 * pow(sin(Bo) , 4) - 10.6 * pow(sin(Bo) , 6) + Xb);
    Xd = pow(Lo , 2) * (1594561.25 + 5336.535 * pow(sin(Bo) , 2) + 26.79 * pow(sin(Bo) , 4) + 0.149 * pow(sin(Bo) , 6) + Xc);
    return 6367558.4968 * Bo - sin(Bo * 2) * (16002.89 + 66.9607 * pow(sin(Bo) , 2) + 0.3515 * pow(sin(Bo) , 4) - Xd);

def SK42LTOY( B, L, H) :   #lat, long
    No = int((6 + L) / 6. )
    Lo = (L - (3 + 6 * (No - 1))) / 57.29577951;
    Bo = B * Pi / 180;
    Ya = pow(Lo , 2) * (79690 - 866190 * pow(sin(Bo) , 2) + 1730360 * pow(sin(Bo) , 4) - 945460 * pow(sin(Bo) , 6));
    Yb = pow(Lo , 2) * (270806 - 1523417 * pow(sin(Bo) , 2) + 1327645 * pow(sin(Bo) , 4) - 21701 * pow(sin(Bo) , 6) + Ya);
    Yc = pow(Lo , 2) * (1070204.16 - 2136826.66 * pow(sin(Bo) , 2) + 17.98 * pow(sin(Bo) , 4) - 11.99 * pow(sin(Bo) , 6) + Yb);
    return (5 + 10 * No) * 100000 + Lo * cos(Bo) * (6378245 + 21346.1415 * pow(sin(Bo) , 2) + 107.159 * pow(sin(Bo) , 4) + 0.5977 * pow(sin(Bo) , 6) + Yc);

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
    Bo = Bi + sin(Bi * 2) * (0.00252588685 - 0.0000149186 * sin(Bi) ** 2 + 0.00000011904 * sin(Bi) ** 4)
    Zo = (Y - (10 * No + 5) * 10 ** 5) / (6378245 * cos(Bo))
    Ba = Zo ** 2 * (0.01672 - 0.0063 * sin(Bo) ** 2 + 0.01188 * sin(Bo) ** 4 - 0.00328 * sin(Bo) ** 6)
    Bb = Zo ** 2 * (0.042858 - 0.025318 * sin(Bo) ** 2 + 0.014346 * sin(Bo) ** 4 - 0.001264 * sin(Bo) ** 6 - Ba)
    Bc = Zo ** 2 * (0.10500614 - 0.04559916 * sin(Bo) ** 2 + 0.00228901 * sin(Bo) ** 4 - 0.00002987 * sin(Bo) ** 6 - Bb)
    dB = Zo ** 2 * sin(Bo * 2) * (0.251684631 - 0.003369263 * sin(Bo) ** 2 + 0.000011276 * sin(Bo) ** 4 - Bc)
    return  (Bo - dB) * 180 / Pi






def SK42YTOL(X, Y, Z) :
     No = Y * 10 ** -6
     No = int(No)
     Bi = X / 6367558.4968
     Bo = Bi + sin(Bi * 2) * (0.00252588685 - 0.0000149186 * sin(Bi) ** 2 + 0.00000011904 * sin(Bi) ** 4)
     Zo = (Y - (10 * No + 5) * 10 ** 5) / (6378245 * cos(Bo))
     La = Zo ** 2 * (0.0038 + 0.0524 * sin(Bo) ** 2 + 0.0482 * sin(Bo) ** 4 + 0.0032 * sin(Bo) ** 6)
     Lb = Zo ** 2 * (0.01225 + 0.09477 * sin(Bo) ** 2 + 0.03282 * sin(Bo) ** 4 - 0.00034 * sin(Bo) ** 6 - La)
     Lc = Zo ** 2 * (0.0420025 + 0.1487407 * sin(Bo) ** 2 + 0.005942 * sin(Bo) ** 4 - 0.000015 * sin(Bo) ** 6 - Lb)
     Ld = Zo ** 2 * (0.16778975 + 0.16273586 * sin(Bo) ** 2 - 0.0005249 * sin(Bo) ** 4 - 0.00000846 * sin(Bo) ** 6 - Lc)
     dL = Zo * (1 - 0.0033467108 * sin(Bo) ** 2 - 0.0000056002 * sin(Bo) ** 4 - 0.0000000187 * sin(Bo) ** 6 - Ld)
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
        co.sin_lat_center_rad = sin ( co.lat_center_rad )
        co.cos_lat_center_rad = cos ( co.lat_center_rad )


def LatLonToAzimut ( lat_grad, lon_grad ) :     # B,  L
          lo = lon_grad * RADpGRAD
          la = lat_grad * RADpGRAD
          sin_la = sin ( la )
          cos_la = cos ( la )
          loMlon_center_rad = lo-co.lon_center_rad
          cos_loMlon_center_rad = cos(loMlon_center_rad)
          Z = sin_la * co.sin_lat_center_rad + cos_la * co.cos_lat_center_rad * cos_loMlon_center_rad
          if  Z < 0 :
              km_x = None 
              km_y = None
          else :    
              km_x = cos_la * sin(loMlon_center_rad) * EARTH
              km_y = EARTH * (sin_la * co.cos_lat_center_rad - cos_la * co.sin_lat_center_rad * cos_loMlon_center_rad )
          return km_x, km_y


