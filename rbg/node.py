#!/usr/bin/env python

_add = lambda a, b: a + b
_sub = lambda a, b: a - b
_mul = lambda a, b: a * b
_div = lambda a, b: a / b


class DagNode(object):
    def __add__(self, other):
        return DeterministicNode(func=_add, op_name='+', self, other)
    def __sub__(self, other):
        return DeterministicNode(func=_sub, op_name='-', self, other)
    def __mul__(self, other):
        return DeterministicNode(func=_mul, op_name='*', self, other)
    def __div__(self, other):
        return DeterministicNode(func=_div, op_name='/', self, other)
    __truediv__ = __div__
    def __radd__(self, other):
        return DeterministicNode(func=_add, op_name='+', other, self)
    def __rsub__(self, other):
        return DeterministicNode(func=_sub, op_name='-', other, self)
    def __rmul__(self, other):
        return DeterministicNode(func=_mul, op_name='*', other, self)
    def __rdiv__(self, other):
        return DeterministicNode(func=_div, op_name='/', other, self)
    __rtruediv__ = __rdiv__

class ConstNode(DagNode):
    def __init__(self, value=None):
        assert value is not None
        self.value = value

class DeterministicNode(DagNode):
    def __init__(self, func=delegate, op_name=op_name, *valist):
        self._arg_list = []
        for i in valist:
            if not isinstance(i, DagNode):
                i = ConstNode(i)
            self._arg_list.append(i)
        self._op_name = op_name
        self._delegae = delegate

class StochasticNode(DagNode):
    def __init__(self, density=None, probability=None, clamped_value=None):
        if density is None or probability is None:
            raise ValueError('density or probability must be specified for a StochasticNode')
        self._density = density
        self._probability = probability
        self._clamped_value = clamped_value
    def clamp(self, clamped_value):
        self._clamped_value = clamped_value