#!/usr/bin/env python
from rbg.node import StochasticNode, DagNode, ConstNode

class ProbabilityDistribution(DagNode):
    def __init__(self, args):
        a = []
        for i in args:
            if not isinstance(i, DagNode):
                i = ConstNode(i)
            a.append(i)
        DagNode.__init__(self, par=a)
        self._args = list(a)
    def create(self):
        return StochasticNode(density=self, par=self)
    def datum(self, value):
        sn = self.create()
        sn.clamp(value)
        return sn
    def descrip(self):
        arg_str_list = []
        for n, arg_name in enumerate(self.arg_names()):
            arg = self._args[n]
            arg_str_list.append('{}={}'.format(arg_name, arg.brief_descrip()))
        return '{}({})'.format(self._NAME, ', '.join(arg_str_list))
    def arg_names(self):
        return self._ARG_NAME_LIST

class Gamma(ProbabilityDistribution):
    _NAME = 'Gamma'
    _ARG_NAME_LIST = ('alpha', 'beta')
    def __init__(self, alpha=None, beta=None):
        if alpha is None or beta is None:
            raise ValueError('alpha and beta must be specified for a Gamma')
        ProbabilityDistribution.__init__(self, [alpha, beta])
        self._alpha, self._beta = self._args

class Exponential(ProbabilityDistribution):
    _NAME = 'Exponential'
    _ARG_NAME_LIST = ('_lambda',)
    def __init__(self, _lambda=None):
        if _lambda is None:
            raise ValueError('_lambda must be specified for a Exponential')
        ProbabilityDistribution.__init__(self, [_lambda])
        self._lambda = self._args[0]

class LogNormal(ProbabilityDistribution):
    _NAME = 'LogNormal'
    _ARG_NAME_LIST = ('mu', 'sigma')
    def __init__(self, mu=None, sigma=None):
        if mu is None or sigma is None:
            raise ValueError('mu and sigma must be specified for a LogNormal')
        ProbabilityDistribution.__init__(self, [mu, sigma])
        self._mu, self._sigma = self._args
