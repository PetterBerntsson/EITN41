#!/usr/bin/env python

from pcapfile import savefile
import re

test = 2

if test == 1:
    testcap = open('cia.log.1337.pcap', 'rb')
    capfile = savefile.load_savefile(testcap, layers=2, verbose=True)
    testcap.close()

    nazirIP = "159.237.13.37"
    mixIP = "94.147.150.188"

    nbrPartners = 2


else:

    testcap = open('cia.log.1339.pcap', 'rb')
    capfile = savefile.load_savefile(testcap, layers=2, verbose=True)
    testcap.close()

    nazirIP = "161.53.13.37"
    mixIP = "11.192.206.171"
    nbrPartners = 12


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
# Last batch is skipped otherwise
if nazirIP in source_set:
    long_set.append(batch_set)

    #print('{}\t\t{}\t{}\t{}\t{}'.format(timestamp, eth_src, eth_dst, ip_src, ip_dst))

long_set_copy = long_set.copy()
check_set = long_set_copy.pop(0)
union_set = check_set.copy()
mes_list = list()
mes_list.append(check_set)

for batch in long_set_copy:
    if union_set.isdisjoint(batch):
        union_set = union_set.union(batch)
        mes_list.append(batch)
        check_set = batch.copy()
        nbrPartners -= 1

    if nbrPartners == 0:
        break
print("Number ME sets: " + str(len(mes_list)))

singleton_list = list()

for mes_set in mes_list:

    # For some reason, you cant mutate a set you iterate
    temp_mes_set = mes_set.copy()

    rest_union = union_set.symmetric_difference(temp_mes_set.copy())

    for batch in long_set:
        if batch.isdisjoint(rest_union):
            temp_mes_set = temp_mes_set.intersection(batch)


    singleton_list.append(temp_mes_set)



partners = list()

for unit_set in singleton_list:
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
