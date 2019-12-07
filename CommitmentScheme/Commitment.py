import hashlib
from collections import defaultdict

# v is either 1 or 0
v = 1

# bit limit
k_limit = 16

x_limit = 16

concat = ""
coll_dict = defaultdict(int)
collisions_arr = list()
collisions = 0
hash_res = ""

for x_length in range(x_limit):
    for k in range(2**k_limit):

        concat = str(v) + " " + str(k)

        hash_res = hashlib.sha1(concat.encode()).hexdigest()[:x_length]
        coll_dict[hash_res] += 1

    for key in coll_dict:
        if coll_dict.get(key) > 1:
            collisions += coll_dict.get(key)

    coll_dict.clear()
    coll_dict = defaultdict(int)
    collisions_arr.append(collisions)
    collisions = 0

for i in range(len(collisions_arr)):
    print("X length = " + str(i) + " - " + "Number collisions = " + str(collisions_arr.pop(0)))


# yaas queen!
# To break the binding property, we need to find a value k, where h(0,k) = h(1,k) Probably a false statement though