#!/usr/bin/env python
import math
from rbg.node import ConstNode, DeterministicNode

def _gen_svf(v, delegate, op_name):
    return DeterministicNode(func=delegate, op_name=op_name, v)

def log(v):
    return _gen_svf(v, math.log, 'log')

def exp(v):
    return _gen_svf(v, math.exp, 'exp')
