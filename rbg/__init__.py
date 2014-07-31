from cStringIO import StringIO
import codecs


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

def generate(node, var_name_dict, file_stem=None, file_path=None, file_stream=None):
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
        _generate(node, var_name_dict, file_stream)
        if ret_str:
            return file_stream.getvalue()
    finally:
        if opened:
            file_stream.close()
