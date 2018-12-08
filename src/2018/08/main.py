from collections import namedtuple

Header = namedtuple('Header', 'child_count, metadata_count')
Node = namedtuple('Node', 'name, header, children, metadata')


def main():
    with open('input') as f:
        line = f.readline()

    tree_definition = [int(n) for n in line.split()]

    metadata_count = count_metadata(tree_definition)
    assert metadata_count == 45868
    print('Answer part 1: {}'.format(metadata_count))


def count_metadata(tree_definition):
    first_node = Node(0, Header(tree_definition[0], tree_definition[1]), [], [])

    nodes = {first_node.name: first_node}

    commands = list(generate_node_commands(first_node))
    idx = 2

    # Parse tree definition
    while commands:
        command = commands.pop()
        if command[0] == 'parse_child':
            child_node = Node(len(nodes), Header(tree_definition[idx], tree_definition[idx + 1],), [], [])
            commands.extend(generate_node_commands(child_node))
            nodes[child_node.name] = child_node
            idx += 2
        else:
            assert command[0] == 'parse_metadata'
            node = command[1]
            node.metadata.extend(tree_definition[idx:idx + node.header.metadata_count])
            idx += node.header.metadata_count

    return sum(sum(node.metadata) for node in nodes.values())


def generate_node_commands(node):
    yield 'parse_metadata', node
    for i in range(node.header.child_count):
        yield 'parse_child', node


assert count_metadata([2, 3, 0, 3, 10, 11, 12, 1, 1, 0, 1, 99, 2, 1, 1, 2]) == 138

if __name__ == '__main__':
    main()
