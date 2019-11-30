from random import random

coin_dict = {}

# bits per coin
u = 17

# pre-images needed per coin (bucket depth)
k = 5

# coins to generate
c = 1

# acceptable standard deviation
s = 2590

def main():

    s_current = 0
    epochs = 0
    data = []
    mean = 0
    sum = 0
    ran = False

    while True:

        epochs += 1
        data_point = find_collisions()

        if epochs == 1:
            data.append(data_point)
            sum += data_point
            epochs += 1
            data_point = find_collisions()

        data.append(data_point)

        sum += data_point
        mean = sum/epochs


        sum_s = 0
        for x in data:
            sum_s += (x - mean)**2

        temp = ((sum_s/(epochs-1))**0.5)
        s_current = 3.66*temp/(epochs**0.5)
        coin_dict.clear()

        # set to appropriate amount, the smaller test cases %100, bigger cases %10 or %1
        if epochs%1 == 0:
            print("Current deviation: " + str(s_current))

        if s_current < s and ran:

            print("\n")
            print("------------------------------------------------------")

            print("mean iterations: " + str(mean))
            print("standard deviation: " + str(s_current))
            print("epochs: " + str(epochs))
            break

        ran = True





def find_collisions():
    # buckets to generate
    b = 2 ** u

    collisions = 0
    iterations = 0
    while collisions < c:
        i = int(random() * b)
        coin_dict[i] = coin_dict.get(i, 0) + 1
        iterations += 1

        # collisions should only happen once per bucket, then the bucket is spent (no need to reset, the statement only happens once per bucket)
        if coin_dict[i] == k:
            collisions += 1

    return iterations

if __name__ == "__main__":
    main()