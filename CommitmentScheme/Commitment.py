import hashlib
from collections import defaultdict

# v is either 1 or 0
v = 1

# bit limit
k_limit = 16

x_limit = 16

concat = ""
dict = defaultdict(int)
collisions_arr = list()
collisions = 0

for x_length in range(x_limit):
    for k in range(2**k_limit):

        concat = str(v) + " " + str(k)

        hash = hashlib.sha1(concat.encode()).hexdigest()[:x_length]
        dict[hash] += 1


    for key in dict:
        if dict.get(key) > 1:
            collisions+=1

    collisions_arr.append(collisions)
    collisions = 0

for i in range(len(collisions_arr)):
    print("X length = " + str(i) + " - " + "Number collisions = " + str(collisions_arr.pop()))


# yaas queen!
# To break the binding property, we need to find a value k, where h(0,k) = h(1,k) Probably a false statement though