import hashlib
from collections import defaultdict

# v is either 1 or 0
v = 0

# bit limit
k_limit = 16

x_limit = 16

concat = ""
coll_dict = defaultdict(int)
zero_dict = defaultdict(bool)
one_dict = defaultdict(bool)
collisions_arr = list()
collisions = 0
hash_res = ""

for x_length in range(x_limit):

    v = 0

    # Basically, the 16 bits are simulated, its not important that k is explicitly binary
    for k in range(2**k_limit):

        # We add space, though it makes no difference, but if v could be larger, "v0k0" could be equal to "v1k1",
        # though "v0 k0" is never equal to "v1 k1". Basically we avoid "simple" collisions
        concat = str(v) + " " + str(k)

        hash_res = hashlib.sha1(concat.encode()).hexdigest()[:x_length]
        zero_dict[hash_res] = True

    v = 1

    for k in range(2**k_limit):

        concat = str(v) + " " + str(k)

        hash_res = hashlib.sha1(concat.encode()).hexdigest()[:x_length]
        one_dict[hash_res] = True

    for key in zero_dict:
        if one_dict[key]:
            collisions += 1

    zero_dict = defaultdict(bool)
    one_dict = defaultdict(bool)
    collisions_arr.append(collisions)


    # No point to continue
    if collisions == 0:
        break

    collisions = 0


for i in range(len(collisions_arr)):
    colls = collisions_arr.pop(0)
    print("X length = " + str(i) + " "*(3 - len(str(i))) + " - " + "Number collisions = " + str(colls) + " "*(10 - len(str(colls)))
          + "\t\t Out of " + str(16**i) + " "*(25 - len(str(16**i))) + "values \t" + "Probability: " + str(100*colls/(16**i)) + "%")

print("\nRemaining values give probability 0%")

# To break the binding property, we need to find a value k, where h(0,k1) = h(1,k2)