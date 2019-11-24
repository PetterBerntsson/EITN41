import hashlib

def readFile(file):
    with open(file, "r") as f:
        return f.read().split()

# part 1
def spv(file):
    data = readFile(file)
    
    hashgen = data.pop(0)
    for node in data:
        concat = hashgen + node[1:] if node[0] == "R" else node[1:] + hashgen
        hashgen = hashlib.sha1(bytearray.fromhex(concat)).hexdigest()
        # print(hashgen)
    return hashgen

# part 2
def fullnode(file):
    data = readFile(file)
    i = int(data.pop(0))
    j = int(data.pop(0))

    leaves = [Node(name) for name in data]

    root = buildTree(leaves)
    pathnode = getPathNode(leaves, i, j)
    return leaves, pathnode, root

def buildTree(layerNodes):
    if len(layerNodes) == 1:
        return layerNodes[0].name
    nodes = layerNodes.copy()
    nextGen = []
    while len(nodes) > 0:
        if len(nodes) == 1:
            l = nodes.pop(0)
            r = Node(l.name)
        else:
            l = nodes.pop(0)
            r = nodes.pop(0)
        l.setPos("L")
        l.setSibling(r)
        r.setPos("R")
        r.setSibling(l)

        parent = genParent(l.name, r.name)
        l.setParent(parent)
        r.setParent(parent)
        nextGen.append(parent)

    return buildTree(nextGen)

def genParent(childL, childR):
    return Node(hashlib.sha1(bytearray.fromhex(childL + childR)).hexdigest())

class Node:
    def __init__(self, name):
        self.name = name
        self.parent = None
        self.pos = ""
        self.sibling = None

    def setParent(self, name):
        self.parent = name

    def setPos(self, pos):
        self.pos = pos

    def setSibling(self, node):
        self.sibling = node

def getPathNode(tree, leafIndex, nodeIndex):

    node = tree[leafIndex]
    merklepath = []
    while node.parent != None:
        merklepath.append(node.sibling.pos + node.sibling.name)
        node = node.parent
    print(merklepath)
    return merklepath[::-1][nodeIndex - 1]

# för skojs skull ------------------------------------
def printTree(nodes):
    indent = (int(len(nodes[0].name)/2) + 4) * " "
    level = 0
    printLayer(nodes, level, indent)

def printLayer(nodes, level, indent):
    if nodes[0] == None:
        return
    layer = "" + indent * level
    nextLayer = []
    for i, node in enumerate(nodes):
        layer += "    " + node.pos + node.name
        if i%2 == 0:
            nextLayer.append(node.parent)
    level += 1
    print(layer)
    printLayer(nextLayer, level, indent)
# ----------------------------------------------------

if __name__ == "__main__":
    # part 1
    # print("Merkle root:", spv("data"))

    # part 2
    tree, pathnode, root = fullnode("fullnode_data")
    print("\nRoot:", root)
    print("Merkele path node || root:", pathnode + root)