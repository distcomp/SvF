# -*- coding: UTF-8 -*-
import sys
path_SvF = "/home/sokol/D/SvF/"
sys.path.append("/home/sokol/D/SvF/SvFlib")
sys.path.append(path_SvF + "pyomo-everest/python-api")
sys.path.append(path_SvF + "pyomo-everest/ssop")
import COMMON as SvF
SvF.path_SvF = path_SvF
SvF.tmpFileDir = SvF.path_SvF + 'TMP/'
from CVSets import *
from Table  import *
from Task   import *
from MakeModel import *
from GIS import *

SvF.Task = TaskClass()
Task = SvF.Task
SvF.mngF = 'MAN-data.mng'
SvF.TaskName="2Body3D"; 
DB = Table ( '../4bdn-1_0.9_0.2_0.06-abc.xlsx','DB','t,x1,y1,z1,x2,y2,z2' )
t = Set('t',SvF.currentTab.dat('t')[:].min(),SvF.currentTab.dat('t')[:].max(),0.01,'','t')
Plot( [ [ DB.dat('t'), DB.dat('x1'), 'lw=0', 'c=r', "marker='o'", 'ms=2', "label='x1-data'", "xlab='t'", 'xlab_x=1.01', "ylab='x1,y1,z1'"], [DB.dat('t'), DB.dat('y1'), 'lw=0', 'c=g', "marker='o'", 'ms=2', "label='x1-data'"], [DB.dat('t'), DB.dat('z1'), 'lw=0', 'c=b', "marker='o'", 'ms=2', "label='z1-data'"] ] )
Plot( [ [ DB.dat('t'), DB.dat('x2'), 'lw=0', 'c=r', "marker='o'", 'ms=2', "label='x2-data'", "xlab='t'", 'xlab_x=1.01', "ylab='x2,y2,z2'"], [DB.dat('t'), DB.dat('y2'), 'lw=0', 'c=g', "marker='o'", 'ms=2', "label='x2-data'"], [DB.dat('t'), DB.dat('z2'), 'lw=0', 'c=b', "marker='o'", 'ms=2', "label='z2-data'"] ] )
P1 = Polyline([DB.dat('x1')[0]],[DB.dat('y1')[0]], None, "P1")
P2 = Polyline([DB.dat('x2')[0]],[DB.dat('y2')[0]], None, "P2")
P1yz = Polyline([DB.dat('y1')[0]],[DB.dat('z1')[0]], None, "P1yz")
P2yz = Polyline([DB.dat('y2')[0]],[DB.dat('z2')[0]], None, "P2yz")
Plot( [ [ DB.dat('x1'), DB.dat('y1'), 'lw=0', 'c=red', "marker='o'", 'ms=2', "label='Data1'", "xlab='x'", 'xlab_x=1.01', "ylab='y'"], [P1, 'ms=5', "label=''"], [DB.dat('x2'), DB.dat('y2'), 'lw=0', 'c=green', "marker='o'", 'ms=2', "label='Data2'"], [P2, 'ms=5', "label=''"] ] )
Plot( [ [ DB.dat('y1'), DB.dat('z1'), 'lw=0', 'c=red', "marker='o'", 'ms=2', "label='Data1'", "xlab='y'", 'xlab_x=1.01', "ylab='z'"], [P1yz, 'ms=5', "label=''"], [DB.dat('y2'), DB.dat('z2'), 'lw=0', 'c=green', "marker='o'", 'ms=2', "label='Data2 '"], [P2yz, 'ms=5', "label=''"] ] )

if SvF.ShowAll:  input("         Нажмите ENTER, чтобы продолжить (закрыть все графики) ")