#!/usr/bin/env python
import math
from rbg.node import ConstNode, DeterministicNode

def _gen_svf(v, delegate, op_name):
    return DeterministicNode(delegate, op_name, v)

def _gen_tvf(left, right, delegate, op_name):
    return DeterministicNode(delegate, op_name, left, right)

def log(v):
    return _gen_svf(v, math.log, 'log')

def exp(v):
    return _gen_svf(v, math.exp, 'exp')

def power(base, exponent):
    return _gen_tvf(base, exponent, pow, 'pow')
