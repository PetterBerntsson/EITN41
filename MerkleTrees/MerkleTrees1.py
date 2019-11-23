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
    i = data.pop(0)
    j = data.pop(0)

    leaves = [Node(name) for name in data]

    buildTree(leaves)
    return leaves

def buildTree(layerNodes):
    nodes = layerNodes.copy()
    nextGen = []
    if len(nodes) == 1:
        return
    while len(nodes) > 0:
        if len(nodes) == 1:
            l = nodes.pop(0)
            r = l
            l.setPos("(pos n/a)") # only child
        else:
            l = nodes.pop(0)
            r = nodes.pop(0)
            l.setPos("L")
            r.setPos("R")
        

        parent = genParent(l.name, r.name)
        l.setParent(parent)
        r.setParent(parent)
        nextGen.append(parent)

    buildTree(nextGen)

def genParent(childL, childR):
    return Node(hashlib.sha1(bytearray.fromhex(childL + childR)).hexdigest())
       

class Node:
    def __init__(self, name):
        self.name = name
        self.parent = None
        self.pos = ""

    def setParent(self, name):
        self.parent = name

    def setPos(self, pos):
        self.pos = pos

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
        layer += "    " + node.pos + node.name + "    "
        if i%2 == 0:
            nextLayer.append(node.parent)
    level += 1
    print(layer)
    printLayer(nextLayer, level, indent)
# ----------------------------------------------------

if __name__ == "__main__":
    # print("Merkle root:", spv("data"))

    tree = fullnode("fullnode_data")
    printTree(tree)