import random

from pcapfile import savefile

testcap = open('cia.log.1339.pcap', 'rb')
capfile = savefile.load_savefile(testcap, layers=2, verbose=True)
testcap.close()

# nazirIP = "159.237.13.37"
# mixIP = "94.147.150.188"
# nbrPartners = 2

nazirIP = "161.53.13.37"
mixIP = "11.192.206.171"
nbrPartners = 12

# print the packets
# print ('timestamp\teth src\t\t\teth dst\t\t\tIP src\t\tIP dst')
# for pkt in capfile.packets:
#     timestamp = pkt.timestamp
#     # all data is ASCII encoded (byte arrays). If we want to compare with strings
#     # we need to decode the byte arrays into UTF8 coded strings
#     eth_src = pkt.packet.src.decode('UTF8')
#     eth_dst = pkt.packet.dst.decode('UTF8')
#     ip_src = pkt.packet.payload.src.decode('UTF8')
#     ip_dst = pkt.packet.payload.dst.decode('UTF8')
#     print ('{}\t\t{}\t{}\t{}\t{}'.format(timestamp, eth_src, eth_dst, ip_src, ip_dst))

batchesFromMix = []
allBatchesFromMix = []
batchFromMix = set()
nazirPackage = False
for pkt in capfile.packets:
    if pkt.packet.payload.src.decode('UTF8') == mixIP:
        batchFromMix.add(pkt.packet.payload.dst.decode('UTF8'))
    else:
        if pkt.packet.payload.src.decode('UTF8') == nazirIP:
            nazirPackage = True
        if batchFromMix:
            allBatchesFromMix.append(batchFromMix)
            if nazirPackage:
                batchesFromMix.append(batchFromMix)
            batchFromMix = set()
            nazirPackage = False
# end case
if batchFromMix and nazirPackage:
    batchesFromMix.append(batchFromMix)

#------------create disjoint set----------------------

unionBatch = batchesFromMix.copy().pop(0)
disjointList = [unionBatch]
for batch in batchesFromMix:
    if len(disjointList) == nbrPartners:
        break
    if unionBatch.isdisjoint(batch):
        disjointList.append(batch)
        unionBatch = unionBatch.union(batch)

#------------reduce---------------------------------

# for x, rx in enumerate(disjointList):
#     # print("---------------------")
#     restUnion = unionBatch ^ rx

#     for r in batchesFromMix:
#         if r.isdisjoint(restUnion) and rx.intersection(r):
#             rx = rx.intersection(r)
#             disjointList[x] = rx
#             # print(len(rx))

#----------------------------------------------------

for r in batchesFromMix:
    for x, rx in enumerate(disjointList):
        disjoint = True

        if rx.intersection(r):

            for rj in disjointList:
                if rj == rx:
                    continue

                if not r.isdisjoint(rj):
                    disjoint = False

            if disjoint:
                rx = rx.intersection(r)
                disjointList[x] = rx
    
    done = True
    for batch in disjointList:
        if len(batch) != 1:
            done = False
    if done:
        break

for disj in disjointList:
    print("'Singleton' length:", len(disj), disj)






dec_sum = 0
for singelton in disjointList:
    partner = next(iter(singelton))

    ipSplit = partner.split(".")
    hexnum = "0x"
    for num in ipSplit:
        temp = hex(int(num))[2:]
        temp = (2 - len(temp)) * "0" + temp
        hexnum += temp

    dec_sum += int(hexnum, 16)

print(dec_sum)
