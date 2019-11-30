SA = 0x684F
SB = 0xF666
DA = 0xE4DC
DB = 0xE452
secretMessage = 0xA725
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