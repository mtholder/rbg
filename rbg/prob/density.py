#!/usr/bin/env python
from rbg.node import StochasticNode

class ProbabilityDistribution(object):
    def create(self):
        return StochasticNode(density=self)
    def datum(self, value):
        sn = self.create()
        sn.clamp(value)
        return sn
class Gamma(object):
    def __init__(self, alpha=None, beta=None):
        if alpha is None or beta is None:
            raise ValueError('alpha and beta must be specified for a Gamma')
        self._alpha = alpha
        self._beta = beta

class Exponential(object):
    def __init__(self, _lambda=None):
        if _lambda is None:
            raise ValueError('_lambda must be specified for a Exponential')
        self._lambda = _lambda

class LogNormal(object):
    def __init__(self, mu=None, sigma=None):
        if mu is None or sigma is None:
            raise ValueError('mu and sigma must be specified for a LogNormal')
        self._mu = mu
        self._sigma = sigma
