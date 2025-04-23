from graphviz import Digraph

def visualize_ast(root):
    dot = Digraph()
    counter = [0]

    def next_id():
        counter[0] += 1
        return f"n{counter[0]}"

    def add_node(label):
        nid = next_id()
        dot.node(nid, label)
        return nid

    def walk(node):
        if node is None:
            return add_node("None")

        label = type(node).__name__

        if hasattr(node, 'name'):
            label += f"\\n{node.name}"
        elif hasattr(node, 'expr'):
            label += f"\\n{node.expr}"
        elif hasattr(node, 'value'):
            label += f"\\n{node.value}"

        parent_id = add_node(label)

        # Handle different node types
        if hasattr(node, 'statements'):
            for stmt in node.statements:
                child_id = walk(stmt)
                dot.edge(parent_id, child_id)

        if hasattr(node, 'block'):
            block_id = walk(node.block)
            dot.edge(parent_id, block_id)

        if hasattr(node, 'blk'):
            blk_id = walk(node.blk)
            dot.edge(parent_id, blk_id)

        if hasattr(node, 'args'):
            for arg in node.args:
                child_id = walk(arg)
                dot.edge(parent_id, child_id)

        if hasattr(node, 'expr') and isinstance(node.expr, list):
            for e in node.expr:
                child_id = walk(e)
                dot.edge(parent_id, child_id)
        elif hasattr(node, 'expr') and hasattr(node.expr, '__dict__'):
            child_id = walk(node.expr)
            dot.edge(parent_id, child_id)

        if hasattr(node, 'condition'):
            cond_id = walk(node.condition)
            dot.edge(parent_id, cond_id)

        if hasattr(node, 'count'):
            count_id = walk(node.count)
            dot.edge(parent_id, count_id)

        if hasattr(node, 'var') and isinstance(node.var, str):
            var_id = add_node(f"Var: {node.var}")
            dot.edge(parent_id, var_id)

        return parent_id

    walk(root)
    return dot
