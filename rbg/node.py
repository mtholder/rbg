#!/usr/bin/env python
from rbg.util import get_logger
_LOG = get_logger(__name__)

_add = lambda a, b: a + b
_sub = lambda a, b: a - b
_mul = lambda a, b: a * b
_div = lambda a, b: a / b

_BINARY_OPERATORS = set([_add, _sub, _mul, _div])


def _find_first_anc(nd):
    curr = nd
    while curr._parents:
        curr = curr._parents[0]
    return curr
def _append_ancsubtree_in_postorder(root, post_list, added):
    first_anc = _find_first_anc(root)
    _append_subtree_in_postorder(root, post_list, added, None)

def _append_subtree_in_postorder(curr, post_list, added, barrier=None):
    curr_sib_stack = []
    curr_next_level_stack = []
    while True:
        #_LOG.debug('_append_subtree_in_postorder for {}'.format(curr.brief_descrip()))
        assert isinstance(curr, DagNode)
        if curr not in added:
            if curr is not barrier:
                curr_next_level_stack.append(curr._children)
                #_LOG.debug('  added {} to curr_next_level_stack'.format([i.brief_descrip() for i in curr_next_level_stack[-1]]))
            post_list.append(curr)
            added.add(curr)
        for p in curr._parents:
            if p not in added:
                _append_ancsubtree_in_postorder(p, post_list, added)
        while (not curr_sib_stack) and curr_next_level_stack:
            curr_sib_stack = curr_next_level_stack.pop()
            #_LOG.debug('  new curr_sib_stack is now {} '.format([i.brief_descrip() for i in curr_sib_stack]))
        if curr_sib_stack:
            curr = curr_sib_stack.pop(0)
            #_LOG.debug('  popped curr_sib_stack is now {} '.format([i.brief_descrip() for i in curr_sib_stack]))
        else:
            break

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
    def __contains__(self, n):
        return id(n) in self._memo
    def sorted_node_list(self):
        curr = self._memo[self._parentless[0]]
        if not curr:
            return snl
        snl = []
        seen = set()
        curr = _find_first_anc(curr)
        _append_subtree_in_postorder(curr, snl, seen, barrier=None)
        return snl

_NEXT_INIT_ORDER_INDEX = 0
class DagNode(object):
    def __init__(self, par=None):
        global _NEXT_INIT_ORDER_INDEX
        self._init_order_index = _NEXT_INIT_ORDER_INDEX
        _NEXT_INIT_ORDER_INDEX += 1
        self._children = []
        self._var_name = None
        if par is None:
            self._parents = []
        else:
            if not isinstance(par, list):
                par = [par]
            self._parents = par
        for p in self._parents:
            p._add_child(self)
    def _base_descrip(self):
        return 'id={} #par={} #children{}'.format(id(self), len(self._parents), len(self._children))
    def descrip(self):
        return 'DagNode {}'.format(self._base_descrip())
    def brief_descrip(self):
        return '<{} id={}>'.format(self.__class__.__name__, id(self))
    def _add_child(self, c):
        self._children.append(c)
    def gen_dag(self, memo):
        dag = Dag(memo)
        self._add_to_dag(dag)
        return dag
    def _add_to_dag(self, dag):
        if self in dag:
            return
        #_LOG.debug('_add_to_dag for {}'.format(self.descrip()))
        self._add_node_and_children(dag)
        for p in self._parents:
            p._add_to_dag(dag)
    def _add_node_and_children(self, dag):
        dag.attempt_add_node(self)
        for c in self._children:
            c._add_to_dag(dag)
    def _create_var_name(self, used_names):
        self._var_name = None
        for p in self._parents:
            self._var_name = p._suggest_name_for_child(self, used_names)
            if self._var_name is not None:
                return self._var_name
        for p in self._children:
            self._var_name = p._suggest_name_for_par(self, used_names)
            if self._var_name is not None:
                return self._var_name
        n = '{}_{}'.format(self.short_type_name(), self._init_order_index)
        vn = n
        i = -1
        while vn in used_names:
            i += 1
            vn = n + '_' + str(i) 
        self._var_name = vn
        return vn
    def short_type_name(self):
        return 'dag'
    def get_var_name(self):
        return self._var_name
    var_name = property(get_var_name)
    def _suggest_name_for_child(self, child, used_names):
        return None
    def _suggest_name_for_par(self, par, used_names):
        return None
    def write_self_in_rev_lang(self, stream):
        raise NotImplementedError('{} write_self_in_rev_lang'.format(self.__class__.__name__))


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
        self._value = value
    def descrip(self):
        return 'ConstNode val={} {}'.format(self._value, self._base_descrip())
    def short_type_name(self):
        return 'const'
    def write_self_in_rev_lang(self, stream):
        assert self._var_name
        stream.write('{} <- {}\n'.format(self._var_name, self._value))

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
    def descrip(self):
        arg_str = '[{}]'.format(', '.join([i.brief_descrip() for i in self._arg_list]))
        pref = 'DeterministicNode operation={}'.format(self._op_name)
        suff = self._base_descrip()
        return '{} {} {}'.format(pref, arg_str, suff)
    def short_type_name(self):
        return 'det'
    def write_self_in_rev_lang(self, stream):
        assert self._var_name
        if self._delegate in _BINARY_OPERATORS:
            stream.write('{} := {} {} {}\n'.format(self._var_name,
                                                   self._arg_list[0].var_name,
                                                   self._op_name,
                                                   self._arg_list[1].var_name))
        else:
            a = ', '.join([i._var_name for i in self._arg_list])
            stream.write('{} := {}({})\n'.format(self._var_name, self._op_name, a))

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
    def descrip(self):
        pref = 'StochasticNode'
        if self._clamped_value:
            pref += ' clamped={}'.format(describe_val_or_node(self._clamped_value))
        if self._density:
            p = self._density.brief_descrip()
        else:
            p = self._probability.brief_descrip()
        suff = self._base_descrip()
        return '{} {} {}'.format(pref, p, suff)
    def short_type_name(self):
        return 'stoch'
    def write_self_in_rev_lang(self, stream):
        assert self._var_name
        if self._density:
            p = self._density._def_in_rev_lang()
        else:
            p = self._probability._def_in_rev_lang()
        stream.write('{} ~ {}\n'.format(self._var_name, p))
        if self._clamped_value:
            stream.write('{}.clamp({})\n'.format(self._var_name, self._clamped_value))

def describe_val_or_node(v):
    if isinstance(v, DagNode):
        return v.descrip()
    return str(v)