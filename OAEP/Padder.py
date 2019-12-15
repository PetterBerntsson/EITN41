import math
import hashlib


mgfSeed = '0123456789abcdef'
maskLen = 30

# hLen = 20 for SHA-1
hLen = 20


# implemented according to https://tools.ietf.org/html/rfc8017#appendix-B.2.1
def mgf1(mgfSeed, maskLen):

    t = ''

    for counter in range(math.ceil(maskLen/hLen)):

        # xLen is always 4
        c = i2osp(counter, 4)
        concat = mgfSeed + c

        t = t + hashlib.sha1(bytearray.fromhex(concat)).hexdigest()

    return t[:maskLen*2]


# implemented according to https://tools.ietf.org/html/rfc8017#section-4.1
# modified to return hex string representation
def i2osp(x, xLen):
    if x >= 256**xLen:
        raise ValueError("integer too large")
    digits = []

    while x:
        digits.append(int(x % 256))
        x //= 256

    for i in range(xLen - len(digits)):
        digits.append(0)

    digits = digits[::-1]

    # return digits if you want a list representation
    tot_hex_string = ''

    for i in range(len(digits)):
        hex_string = hex(digits[i])[2:]
        if len(hex_string) < 2:
            hex_string = '0' + hex_string
        tot_hex_string = tot_hex_string + hex_string

    return tot_hex_string

print(mgf1(mgfSeed, maskLen))
