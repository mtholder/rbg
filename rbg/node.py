#!/usr/bin/env python

_add = lambda a, b: a + b
_sub = lambda a, b: a - b
_mul = lambda a, b: a * b
_div = lambda a, b: a / b

class Dag(object):
    def __init__(self, memo):
        self._memo = memo
        self._parentless = []
    def attempt_add_node(self, node):
        node_id = id(node)
        if node_id in self._memo:
            return
        self._memo[node_id] = node
        if not node._children:
            self._parentless.append(node_id)

_NEXT_INIT_ORDER_INDEX = 0
class DagNode(object):
    def __init__(self, par=None):
        global _NEXT_INIT_ORDER_INDEX
        self._init_order_index = _NEXT_INIT_ORDER_INDEX
        _NEXT_INIT_ORDER_INDEX += 1
        self._children = []
        if par is None:
            self._parents = []
        else:
            if not isinstance(par, list):
                par = [par]
            self._parents = par
        for p in self._parents:
            p._add_child(self)
    def _add_child(self, c):
        self._children.append(c)
    def gen_dag(self, memo):
        dag = Dag(memo)
        self._add_to_dag(dag)
        return dag
    def _add_to_dag(self, dag, avoid_node=None):
        self._add_node_and_children(dag, child2avoid=avoid_node)
        for p in self._parents:
            if p is not avoid_node:
                p._add_to_dag(dag, avoid_node=self)
    def _add_node_and_children(self, dag, child2avoid=None):
        dag.attempt_add_node(self)
        for c in self._children:
            if c is not child2avoid:
                c._add_to_dag(dag, avoid_node=self)

class OperableDagNode(DagNode):
    def __init__(self, par=None):
        DagNode.__init__(self, par=par)
    def __add__(self, other):
        return DeterministicNode(_add, '+', self, other)
    def __sub__(self, other):
        return DeterministicNode(_sub, '-', self, other)
    def __mul__(self, other):
        return DeterministicNode(_mul, '*', self, other)
    def __div__(self, other):
        return DeterministicNode(_div, '/', self, other)
    __truediv__ = __div__
    def __radd__(self, other):
        return DeterministicNode(_add, '+', other, self)
    def __rsub__(self, other):
        return DeterministicNode(_sub, '-', other, self)
    def __rmul__(self, other):
        return DeterministicNode(_mul, '*', other, self)
    def __rdiv__(self, other):
        return DeterministicNode(_div, '/', other, self)
    __rtruediv__ = __rdiv__

class ConstNode(OperableDagNode):
    def __init__(self, value=None):
        OperableDagNode.__init__(self)
        assert value is not None
        self.value = value

class DeterministicNode(OperableDagNode):
    def __init__(self, delegate, op_name, *valist):
        a = []
        for i in valist:
            if not isinstance(i, DagNode):
                i = ConstNode(i)
            a.append(i)
        OperableDagNode.__init__(self, par=list(a))
        self._arg_list = a
        self._op_name = op_name
        self._delegate = delegate

class StochasticNode(OperableDagNode):
    def __init__(self, density=None, probability=None, clamped_value=None, par=None):
        if density is None and probability is None:
            raise ValueError('density or probability must be specified for a StochasticNode')
        OperableDagNode.__init__(self, par=par)
        self._density = density
        self._probability = probability
        self._clamped_value = clamped_value
    def clamp(self, clamped_value):
        self._clamped_value = clamped_value