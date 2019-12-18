import codecs

# DER integer encoding
def int_hex_encode(integer):
    hex_type = '02'  # INTEGER 0x02

    bin_val = bin(integer)[2:]
    if len(bin_val) % 8 != 0:
        bin_val = (8 - len(bin_val) % 8) * '0' + bin_val

    hex_val = hex(int(bin_val, 2))[2:]
    hex_val = len(hex_val) % 2 * '0' + hex_val
    if bin_val[0] == '1':
        hex_val = '00' + hex_val  # 2 complement zero padding

    hex_len, len_form = hex_len_encode(hex_val)
    # print("type:", hex_type, "length(" + len_form + "):", hex_len, "value:", hex_val)
    
    return hex_type + hex_len + hex_val


# definite form length encoding
def hex_len_encode(hex_val):
    hex_len = hex(int(len(hex_val) / 2))[2:]
    hex_len = len(hex_len) % 2 * '0' + hex_len
    len_form = "short definite form"

    if len(hex_val) / 2 > 127:  # long definite form if #value octets > 127
        len_form = "long definite form"
        bin_hex_len_len = bin(int(len(hex_len) / 2))[2:]
        bin_hex_len_len = (7 - len(bin_hex_len_len) %
                           2) * '0' + bin_hex_len_len
        bin_hex_len_len = '1' + bin_hex_len_len
        # first octet starting with 1 and the rest of the bits in the first octet 
        # defines the number of following octets defining the octet length of the value
        hex_len = hex(int(bin_hex_len_len, 2))[2:] + hex_len

    return hex_len, len_form


# extended euclidean algorithm
def egcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        g, y, x = egcd(b % a, a)
        return g, x - (b // a) * y, y


# modular multiplicative inverse
def modinv(a, m):
    g, x, _ = egcd(a, m)
    if g != 1:
        raise Exception('no modular inverse')
    else:
        return x % m


# DER encoding for RSA private key
def rsa_priv_key(p, q):
    hex_type = '30' # SEQUENCE 0x30
    v = int_hex_encode(0)
    n = int_hex_encode(p*q)
    e = int_hex_encode(65537)
    phi = (p - 1) * (q - 1)
    d = modinv(65537, phi)
    d_hex = int_hex_encode(d)
    p_hex = int_hex_encode(p)
    q_hex = int_hex_encode(q)
    exp1 = int_hex_encode(d % (p - 1))
    exp2 = int_hex_encode(d % (q - 1))
    coeff = modinv(q, p)
    coeff_hex = int_hex_encode(coeff)

    seq_val = v + n + e + d_hex + p_hex + q_hex + exp1 + exp2 + coeff_hex
    seq_len, len_form = hex_len_encode(seq_val)

    print("T:", hex_type, "L:", seq_len, "V:", seq_val)
    hex_encoding = hex_type + seq_len + seq_val
    base64_encoding = codecs.encode(codecs.decode(hex_encoding, 'hex'), 'base64').decode()

    return hex_encoding, base64_encoding


# quiz question 1: encode integer
# print(int_hex_encode(161863091426469985001358176493540241719547661391527305133576978132107887717901972545655469921112454527920502763568908799229786534949082469136818503316047702610019730504769581772016806386178260077157969035841180863069299401978140025225333279044855057641079117234814239380100022886557142183337228046784055073741))

# quiz question 2: encode RSA private key
rsa_hex, rsa_b64 = rsa_priv_key(2530368937, 2612592767)
print("DER encoded RSA private key in hex:", rsa_hex)
print("DER encoded RSA private key in b64:", rsa_b64)
