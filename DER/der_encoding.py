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
        print(hex_len, len(hex_val)/2)
        len_form = "long definite form"
        bin_hex_len_len = bin(int(len(hex_len) / 2))[2:]
        print(bin_hex_len_len, len(bin_hex_len_len))
        bin_hex_len_len = (7 - len(bin_hex_len_len)) * '0' + bin_hex_len_len
        bin_hex_len_len = '1' + bin_hex_len_len
        print(bin_hex_len_len, "\n")

        # first octet starting with 1 and the rest of the bits in the first octet
        # defines the number of following octets defining the octet length of the value
        hex_len = hex(int(bin_hex_len_len, 2))[2:] + hex_len
        # print(hex_len, "\n")

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
    hex_type = '30'  # SEQUENCE 0x30
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

    # print("T:", hex_type, "L:", seq_len, "V:", seq_val)
    hex_encoding = hex_type + seq_len + seq_val
    print(len(seq_len), seq_len)
    base64_encoding = codecs.encode(codecs.decode(
        hex_encoding, 'hex'), 'base64').decode()

    return hex_encoding, base64_encoding


# quiz question 1: encode integer
# print(int_hex_encode(152482328196495022806892137829964892542509320800276950282095732553763624528669188110962102894036698027122251149089007046808495828083997541887435942011830755899544404815825750422468299995556514726333535881694505256190163616575654042023843956094494385008384304569645597012571027621213061798814023199266195664899))

# quiz question 2: encode RSA private key
rsa_hex, rsa_b64 = rsa_priv_key(164114594813800307418447673273331457802487402173218084522602279570759004943271059687980245867351587073874764332560761774240994382474441220210511471982863169720786223197663189087845453185199410925726140702115909207384343131130632724527137836874094130746865061867165444262600737519305143603065906576556601467253,
                                138860036995238526080367240083285286681635555273154650324671981431526392420382863540566294084899239184605154847615665762977423503412412956533905723990024164641959322001637368919248262573746614094591422079709594652645576162813156700232309643462640201858941733810450453809169981262133674178293379602902911333927)
print("DER encoded RSA private key in hex:", rsa_hex)
print("DER encoded RSA private key in b64:", rsa_b64)
