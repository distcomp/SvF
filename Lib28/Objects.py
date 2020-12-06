# -*- coding: cp1251 -*-
from __future__ import division

import COMMON as co



class Object :
    def __init__ (self, name, o_type, object) :   #
        self.name   = name
        self.o_type = o_type
        self.object = object



def addObject(name, o_type, object):
    co.Task.Objects.insert(0, Object(name, o_type, object))


def getObject(name):
    for o in co.Task.Objects:
        if o.name == name: return o
    return None



