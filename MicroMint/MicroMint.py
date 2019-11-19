from random import random

coin_dict = {}

# bits per coin
u = 16

# pre-images needed per coin (bucket depth)
k = 2

# coins to generate
c = 10000


def main():
    # buckets to generate
    b = 2**u


    find_collisions()



def find_collisions():
    b = 2 ** u

    collisions = 0
    iterations = 0
    while collisions < c:
        i = int(random() * b)
        coin_dict[i] = coin_dict.get(i, 0) + 1
        iterations = iterations + 1

        if coin_dict[i] >= k:
            collisions = collisions + 1

    print("coins found: " + str(collisions))
    print("iterations: " + str(iterations))

if __name__ == "__main__":
    main()