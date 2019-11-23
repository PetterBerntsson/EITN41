import hashlib

def spv(file):
    f = open(file, "r")
    data = f.read().split()
    f.close()
    
    hashgen = data.pop(0)
    for node in data:
        concat = hashgen + node[1:] if node[0] == "R" else node[1:] + hashgen
        hashgen = hashlib.sha1(bytearray.fromhex(concat)).hexdigest()
        # print(hashgen)
    return hashgen
        
if __name__ == "__main__":
    print("merkle root:", spv("data"))