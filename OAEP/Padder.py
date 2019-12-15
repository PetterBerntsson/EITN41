import math
import hashlib


# implemented according to https://tools.ietf.org/html/rfc8017#appendix-B.2.1
def mgf1(mgfSeed, maskLen):
    t = ''

    if maskLen > ((2 ** 32) * hLen):
        raise ValueError("mask too long")

    for counter in range(math.ceil(maskLen / hLen)):
        # xLen is always 4
        c = i2osp(counter, 4)
        concat = mgfSeed + c

        t = t + hashlib.sha1(bytearray.fromhex(concat)).hexdigest()

    return t[:maskLen * 2]


# implemented according to https://tools.ietf.org/html/rfc8017#section-4.1
# modified to return hex string representation
def i2osp(x, xLen):
    if x >= 256 ** xLen:
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


# implemented according to https://tools.ietf.org/html/rfc8017#section-7.1.1
def oaep_encode(message, seed, L):

    if len(L) > (2**61 - 1):
        raise ValueError("label too long")
    if len(message) > (k - 2*hLen - 2):
        raise ValueError("message too long")

    if L == None:
        L = ''

    lhash = hashlib.sha1(bytearray.fromhex(L)).hexdigest()
    ps = "".zfill((k - int(len(message)/2) - 2*hLen - 2)*2)

    db = lhash + ps + '01' + message

    db_mask = mgf1(str(seed), k-hLen-1)
    masked_db = hex(int(db, 16) ^ int(db_mask, 16))[2:]

    seed_mask = mgf1(str(masked_db), hLen)
    masked_seed = hex(int(str(seed), 16) ^ int(str(seed_mask), 16))[2:]

    em = '00' + str(masked_seed) + str(masked_db)
    return em.zfill(256)


def oaep_decode(encrypted_message):
    print("decode")


#----------------------------------- Test Values ----------------------------------------------------------------------
mgfSeed = '0123456789abcdef'
maskLen = 30

# hLen = 20 for SHA-1
hLen = 20

# default value for L
L = ""

k = 128
message = 'fd5507e917ecbe833878'
seed = '1e652ec152d0bfcd65190ffc604c0933d0423381'
#----------------------------------------------------------------------------------------------------------------------

print(oaep_encode(message, seed, L))