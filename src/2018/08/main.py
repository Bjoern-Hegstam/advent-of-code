from collections import namedtuple

Header = namedtuple('Header', 'child_count, metadata_count')
Node = namedtuple('Node', 'name, header, children, metadata')


def main():
    with open('input') as f:
        line = f.readline()

    tree_definition = [int(n) for n in line.split()]

    root_node, nodes = build_tree(tree_definition)

    metadata_count = count_metadata(nodes)
    assert metadata_count == 45868
    print('Answer part 1: {}'.format(metadata_count))

    node_value = calculate_node_value(root_node)
    assert node_value == 19724
    print('Answer part 2: {}'.format(node_value))


def count_metadata(nodes):
    return sum(sum(node.metadata) for node in nodes.values())


def build_tree(tree_definition):
    root_node = Node(0, Header(tree_definition[0], tree_definition[1]), [], [])

    nodes = {root_node.name: root_node}
    commands = list(generate_node_commands(root_node))

    idx = 2
    while commands:
        command = commands.pop()
        if command[0] == 'parse_child':
            child_node = Node(len(nodes), Header(tree_definition[idx], tree_definition[idx + 1], ), [], [])
            commands.extend(generate_node_commands(child_node))
            nodes[child_node.name] = child_node
            nodes[command[1].name].children.append(child_node)
            idx += 2
        else:
            assert command[0] == 'parse_metadata'
            node = command[1]
            node.metadata.extend(tree_definition[idx:idx + node.header.metadata_count])
            idx += node.header.metadata_count

    return root_node, nodes


def generate_node_commands(node):
    yield 'parse_metadata', node
    for i in range(node.header.child_count):
        yield 'parse_child', node


def calculate_node_value(node):
    if not node.children:
        return sum(node.metadata)

    return sum(calculate_node_value(node.children[idx - 1]) for idx in node.metadata if idx < node.header.child_count + 1)


test_root_node, test_nodes = build_tree([2, 3, 0, 3, 10, 11, 12, 1, 1, 0, 1, 99, 2, 1, 1, 2])
assert count_metadata(test_nodes) == 138
assert calculate_node_value(test_root_node) == 66


if __name__ == '__main__':
    main()
