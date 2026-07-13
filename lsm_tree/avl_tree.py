from collections import deque


class Node:
    def __init__(self, key, val=None):
        self.key = key
        self.val = val

        self.left = None
        self.right = None

        self.height = 1


def height(node):
    return node.height if node else 0


def update_height(node):
    node.height = 1 + max(height(node.left), height(node.right))


def balance(node):
    return height(node.left) - height(node.right)


def right_rotate(z):
    y = z.left
    T3 = y.right

    y.right = z
    z.left = T3

    update_height(z)
    update_height(y)

    return y


def left_rotate(z):
    y = z.right
    T2 = y.left

    y.left = z
    z.right = T2

    update_height(z)
    update_height(y)

    return y


def insert(root, key, val=None):

    if root is None:
        return Node(key, val)

    if key < root.key:
        root.left = insert(root.left, key, val)

    elif key > root.key:
        root.right = insert(root.right, key, val)

    else:
        root.val = val
        return root

    update_height(root)

    b = balance(root)

    # LL
    if b > 1 and key < root.left.key:
        return right_rotate(root)

    # RR
    if b < -1 and key > root.right.key:
        return left_rotate(root)

    # LR
    if b > 1 and key > root.left.key:
        root.left = left_rotate(root.left)
        return right_rotate(root)

    # RL
    if b < -1 and key < root.right.key:
        root.right = right_rotate(root.right)
        return left_rotate(root)

    return root


def inorder(root):
    if root is None:
        return

    inorder(root.left)
    print(root.key, root.val)
    inorder(root.right)


def level_order(root):
    if root is None:
        return

    q = deque([(root, 0)])
    level = 0

    while q:
        node, l = q.popleft()

        if l != level:
            print()
            level = l

        print(node.key, end=" ")

        if node.left:
            q.append((node.left, l + 1))

        if node.right:
            q.append((node.right, l + 1))

    print()