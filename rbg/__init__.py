from cStringIO import StringIO
import codecs
import sys

class MCMC(object):
    def __init__(self, burnin, tuning_freq, generations):
        self.burnin = burnin
        self.tuning_freq = tuning_freq
        self.generations = generations
        self.var_name = '_mcmc'
    def _write_in_rev_lang(self, stream):
        b = '{}.burnin(generations={}, tuningInterval={})\n'
        stream.write(b.format(self.var_name,
                              self.burnin,
                              self.tuning_freq))
        stream.write('{}.run(generations={})\n'.format(
                      self.var_name, self.generations))

class Monitor(object):
    def __init__(self, freq, file_name=None, separator='\t', stream=None, *valist):
        if file_name is None and stream is None:
            raise ValueError('file_name or stream must be specified for a Monitor')
        self.file_name = file_name
        self.stream = stream
        self.separator = separator
        self.freq = freq
        self.args = list(valist)
    def _def_in_rev_lang(self):
        if self.stream is sys.stdout:
            f = 'screenmonitor(printgen={}, separator="{}"'
            f = f.format(self.freq, self.separator)
        else:
            f = 'modelmonitor(printgen={}, separator="{}", filename="{}"'
            f = f.format(self.freq, self.separator, self.file_name)
        if self.args:
            a = ', '.join([i.var_name for i in self.args])
            f = '{}, {})'.format(f, a)
        else:
            f += ')'
        return f

def _generate(node, var_name_dict, stream):
    memo = {}
    dag = node.gen_dag(memo)
    nl = dag.sorted_node_list()
    id2var_name = {}
    from rbg.node import DagNode
    for var_name, var in var_name_dict.items():
        if isinstance(var, DagNode):
            id2var_name[id(var)] = var_name
    used_var_names = {}
    for node in nl:
        vn = id2var_name.get(id(node))
        if vn is not None:
            node._var_name = vn
            used_var_names[var_name] = node
    for node in nl:
        if not node.var_name:
            vn = node._create_var_name(used_var_names)
            used_var_names[vn] = node

    for node in nl:
        node.write_self_in_rev_lang(stream)

def generate(dag_node,
             move_list=None,
             monitors_list=None,
             mcmc=None,
             var_name_dict=None,
             file_stem=None,
             file_path=None,
             file_stream=None,
             suffix=None):
    if var_name_dict is None:
        var_name_dict = {}
    ret_str = False
    opened = False
    if file_stream is None:
        if file_path is None:
            if file_stem is None:
                ret_str = True
                file_stream = StringIO()
            else:
                if file_stem.endswith('.py'):
                    file_path = '{}.Rev'.format(file_stem[:-3])
                else:
                    file_path = file_stem + '.Rev'
        if file_stream is None:
            opened = True
            file_stream = codecs.open(file_path, 'w', encoding='utf8')
    try:
        _generate(dag_node, var_name_dict, file_stream)
        file_stream.write('_model <- model({})\n'.format(dag_node.var_name))
        if move_list:
            for n, m in enumerate(move_list):
                file_stream.write('_moves[{}] <- {}\n'.format((n+1), m._def_in_rev_lang()))
        if monitors_list:
            for n, m in enumerate(monitors_list):
                file_stream.write('_monitors[{}] <- {}\n'.format((n+1), m._def_in_rev_lang()))
        if mcmc:
            file_stream.write('_mcmc <- mcmc(_model, _monitors, _moves)\n')
            mcmc.var_name = '_mcmc'
            mcmc._write_in_rev_lang(file_stream)
        if suffix is not None:
            file_stream.write('\n{}\n'.format(suffix))
        if ret_str:
            return file_stream.getvalue()
    finally:
        if opened:
            file_stream.close()
