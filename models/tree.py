class TreeNode:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None

def inorder_traversal(current_node, depth):
    if current_node is not None:
        inorder_traversal(current_node.left, depth + 1)
        spasi = "   " * depth
        print(spasi + "-> " + current_node.data)
        inorder_traversal(current_node.right, depth + 1)