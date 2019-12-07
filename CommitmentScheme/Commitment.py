import hashlib
from collections import defaultdict
import binascii

# v is either 1 or 0
v = 0

# bit limit
k_limit = 16

# after 24 it stops converging
x_limit = 48

concat = ""
coll_dict = defaultdict(int)
zero_dict = defaultdict(bool)
one_dict = defaultdict(bool)
coll_list = list()
collisions = 0
hash_res = ""

for x_length in range(1, x_limit):

    v = 0
    zero_dict = defaultdict(bool)
    one_dict = defaultdict(bool)

    # Basically, the 16 bits are simulated, its not important that k is explicitly binary
    for k in range(2**k_limit):

        # We add space, though it makes no difference, but if v could be larger, "v0k0" could be equal to "v1k1",
        # though "v0 k0" is never equal to "v1 k1". Basically we avoid "simple" collisions
        concat = str(v) + " " + str(k)

        hash_res = hashlib.sha1(concat.encode()).hexdigest()
        bin_res = (bin(int(hash_res, 16))[2:])[-x_length:]
        zero_dict[bin_res] = True

    v = 1

    for k in range(2**k_limit):

        concat = str(v) + " " + str(k)

        hash_res = hashlib.sha1(concat.encode()).hexdigest()
        bin_res = (bin(int(hash_res, 16))[2:])[-x_length:]
        one_dict[bin_res] = True

    for key in zero_dict:
        if one_dict[key]:
            collisions += 1

    coll_list.append(collisions)


    # No point to continue
    if collisions == 0:
        print("breaking at run " + str(x_length))
        break

    collisions = 0
    print("Run " + str(x_length))

for i in range(1, len(coll_list) + 1):
    colls = coll_list.pop(0)
    print("X length = " + str(i) + " "*(3 - len(str(i))) + " - " + "Number collisions = " + str(colls) + " "*(10 - len(str(colls)))
          +  "Probability: " + str(100*colls/min(2**i, 2**k_limit)) + "%")
    # "\t\t Out of " + str(16**i) + " "*(70 - len(str(16**i))) + "values \t" +

print("\nRemaining values give probability 0%")

# To break the binding property, we need to find a value k, where h(0,k1) = h(1,k2)