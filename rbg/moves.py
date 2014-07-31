#!/usr/bin/env python
class ScaleMove(object):
    def __init__(self, dag_node, size, tune=True, weight=1.0):
        self.dag_node = dag_node
        self.size = size
        self.tune = tune
        self.weight = weight
    def _def_in_rev_lang(self):
        t = 'true' if self.tune else 'false'
        f = 'mvScale({}, lambda={}, tune={}, weight={})'
        return f.format(self.dag_node.var_name, self.size, t, self.weight)
