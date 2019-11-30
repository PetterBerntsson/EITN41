SA = 0x0C73
SB = 0x80C1
DA = 0xA2A9 
DB = 0x92F5
secretMessage = 0x9B57
b = 0

# SA = 0x27C2
# SB = 0x0879
# DA = 0x35F6 
# DB = 0x1A4D
# secretMessage = 0x27BC
# b = 1

SAxorSB = SA ^ SB
combined = (SAxorSB ^ DA) ^ DB

if b:
    output = hex(SAxorSB ^ secretMessage)[2:]
    output = (4 - len(output)) * "0" + output
    print(output)
else:
    print(hex(SAxorSB)[2:] + hex(combined)[2:])
