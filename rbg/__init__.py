from cStringIO import StringIO
import codecs


def _generate(node, stream):
    memo = {}
    dag = node.gen_dag(memo)
    nl = dag.sorted_node_list()
    for node in nl:
        node.write(stream, memo)

def generate(node, file_stem=None, file_path=None, file_stream=None):
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
        _generate(node, file_stream)
        if ret_str:
            return file_stream.getvalue()
    finally:
        if opened:
            file_stream.close()
