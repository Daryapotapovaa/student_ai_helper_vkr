# Задание: обход дерева и поиск путей

class TreeNode:
    def __init__(self, value):
        self.value = value
        self.children = []

    def add_child(self, child):
        self.children.append(child)
        return self


def find_all_paths(node, target, current_path=None):
    if current_path is None:
        current_path = []

    current_path = current_path + [node.value]

    if node.value == target:
        return [current_path]

    if not node.children:
        return []

    paths = []
    for child in node.children:
    child_paths = find_all_paths(child, target, current_path)
        paths.extend(child_paths)

    return paths


def tree_depth(node):
    if not node.children:
        return 0
    return 1 + max(tree_depth(child) for child in node.children)


def count_nodes(node):
    return 1 + sum(count_nodes(child) for child in node.children)


root = TreeNode("A")
b = TreeNode("B")
c = TreeNode("C")
d = TreeNode("D")
e = TreeNode("E")
f = TreeNode("F")

root.add_child(b).add_child(c)
b.add_child(d).add_child(e)
c.add_child(f)

print(f"Глубина дерева: {tree_depth(root)}")
print(f"Количество узлов: {count_nodes(root)}")

paths = find_all_paths(root, "E")
print(f"Пути до E: {paths}")
