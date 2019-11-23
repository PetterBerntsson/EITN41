import hashlib


def MerklePath():

    f = open("data", "r")
    data = f.read().split()
    f.close()

    left = ""
    right = ""
    result = data.pop(0)

    for row in data:

        if row[0] == "R":
            right = row[1:]
            left = result

        if row[0] == "L":
            right = result
            left = row[1:]


        result = hashlib.sha1((left + right).encode()).hexdigest()

    print(result)











if __name__ == "__main__":
    MerklePath()