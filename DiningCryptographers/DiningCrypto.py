SA = 0xBF0D
SB = 0x3C99
DA = 0x186F
DB = 0x2EAD
secretMessage = 0x62AB
b = 0

def padhex(hexnbr):
    return (4 - len(hexnbr)) * "0" + hexnbr

SAxorSB = SA ^ SB
combined = (SAxorSB ^ DA) ^ DB

if b:
    output = padhex(hex(SAxorSB ^ secretMessage)[2:])
else:
    output = padhex(hex(SAxorSB)[2:]) + padhex(hex(combined)[2:])

print(output)