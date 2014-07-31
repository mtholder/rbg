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

class Gamma(ProbabilityDistribution):
    def __init__(self, alpha=None, beta=None):
        if alpha is None or beta is None:
            raise ValueError('alpha and beta must be specified for a Gamma')
        ProbabilityDistribution.__init__(self, [alpha, beta])
        self._alpha, self._beta = self._args

class Exponential(ProbabilityDistribution):
    def __init__(self, _lambda=None):
        if _lambda is None:
            raise ValueError('_lambda must be specified for a Exponential')
        ProbabilityDistribution.__init__(self, [_lambda])
        self._lambda = self._args[0]

class LogNormal(ProbabilityDistribution):
    def __init__(self, mu=None, sigma=None):
        if mu is None or sigma is None:
            raise ValueError('mu and sigma must be specified for a LogNormal')
        ProbabilityDistribution.__init__(self, [mu, sigma])
        self._mu, self._sigma = self._args
