

def int_hex_encode(integer):
    hex_type = '02'  # integer 0x02

    bin_val = bin(integer)[2:]
    bin_val = (4 - len(bin_val) % 4) * '0' + bin_val

    hex_val = hex(int(bin_val, 2))[2:]
    hex_val = len(hex_val) % 2 * '0' + hex_val
    if bin_val[0] == 1:
        hex_val = '00' + hex_val  # 2 complement zero padding

    hex_len = hex(len(hex_val) / 2)[2:]
    hex_len = len(hex_len) % 2 * '0' + hex_len

    if len(bin_val) > 128:  # long definite form
        bin_hex_len_len = bin(len(hex_len) / 2)[2:]
        bin_hex_len_len = (7 - len(bin_hex_len_len) %
                           2) * '0' + bin_hex_len_len
        bin_hex_len_len = '1' + bin_hex_len_len
        # first octet starting with 1 and the rest bits in the first octet defines the number of following octets defining the length of the value
        hex_len = hex(bin_hex_len_len)[2:] + hex_len

    return hex_type + hex_len + hex_val
