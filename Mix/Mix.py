#!/usr/bin/env python

from pcapfile import savefile
import re

testcap = open('cia.log.1337.pcap', 'rb')
capfile = savefile.load_savefile(testcap, layers=2, verbose=True)

#nazirIP = "159.237.13.37"
#mixIP = "94.147.150.188"

nazirIP = "161.53.13.37"
mixIP = "11.192.206.171"
nbrPartners = 2

long_set = list()
old_ip_dst = ""
old_ip_src = ""
batch_set = set()
source_set = set()
new_batch = False

for pkt in capfile.packets:

    timestamp = pkt.timestamp
    # all data is ASCII encoded (byte arrays). If we want to compare with strings
    # we need to decode the byte arrays into UTF8 coded strings
    eth_src = pkt.packet.src.decode('UTF8')
    eth_dst = pkt.packet.dst.decode('UTF8')
    ip_src = pkt.packet.payload.src.decode('UTF8')
    ip_dst = pkt.packet.payload.dst.decode('UTF8')


    if ip_dst == mixIP:
        if new_batch:
            # We will see if the batch is worth adding to the collection
            if nazirIP in source_set:
                long_set.append(batch_set.copy())
            batch_set.clear()
            source_set.clear()
            new_batch = False
        source_set.add(ip_src)
    elif ip_src == mixIP:

        # Some sort of trigger for the new batch, though the new batch started earlier
        new_batch = True
        batch_set.add(ip_dst)


    #print('{}\t\t{}\t{}\t{}\t{}'.format(timestamp, eth_src, eth_dst, ip_src, ip_dst))

intersect_set = set()
disjoint_sets = list()
partners_set = list()
progress = True
while progress:

    # we may have several disjoint sets, so we need to check if we make any progress
    progress = False
    intersect_set = long_set.pop(0)

    for batch in long_set:

        if not batch.isdisjoint(intersect_set):
            progress = True
            intersect_set = batch.intersection(intersect_set)
        else:
            disjoint_sets.append(batch.copy())
    partners_set.append(intersect_set.copy())
    intersect_set.clear()
    long_set.clear()

    # no more disjoint sets, but we still made progress, so break
    if len(disjoint_sets) == 0:
        break
    long_set = disjoint_sets.copy()
    disjoint_sets.clear()


partners = list()

for unit_set in partners_set:
    partners.append(next(iter(unit_set)))

print("Number partners: " + str(len(partners)))
ip_lists = list()
ip_hex = ""
dec_sum = 0

for partner in partners:
    ip_list = partner.split(".")

    for ip_nbr in ip_list:
        ip_hex = ip_hex + hex(int(ip_nbr))[2:]


    dec_sum = dec_sum + int("0x" + ip_hex, 16)
    ip_hex = ""

print(dec_sum)


print("-----------------------------------------------------------------------------------------------------")
print('timestamp\t\teth src\t\t\teth dst\t\t\tIP src\t\tIP dst')
