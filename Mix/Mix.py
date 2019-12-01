from pcapfile import savefile
import sys
import re

test = 2
filepath = ""

if test == 1:
    filepath = 'cia.log.1337.pcap'
    nazirIP = "159.237.13.37"
    mixIP = "94.147.150.188"
    nbrPartners = 2
else:
    filepath = 'cia.log.1339.pcap'
    nazirIP = "161.53.13.37"
    mixIP = "11.192.206.171"
    nbrPartners = 12

long_set = list()
batch_set = set()
source_set = set()
new_batch = False
# --------------------------------------- LEARNING PHASE --------------------------------------------------------------
# --------------------------------------- LOAD BATCHES
with open(filepath, 'rb') as testcap:
    capfile = savefile.load_savefile(testcap, layers=2, verbose=True)
    testcap.close()
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
        long_set.append(batch_set.copy())


# --------------------------------------- SECOND PART OF LEARNING PHASE------------------------------------------------
# We have to start with some set
first_set = long_set.copy().pop(0)
union_set = first_set.copy()
mes_list = list()
mes_list.append(first_set.copy())
# --------------------------------------- GET (NUMBER PARTNERS) DISJOINT SETS
for batch in long_set:
    if union_set.isdisjoint(batch):
        union_set = union_set.union(batch)
        mes_list.append(batch)
        nbrPartners -= 1

    if nbrPartners == 0:
        break

# --------------------------------------- RUN INTERSECTIONS -----------------------------------------------------------
partners = list()
# All sets in mes_list have been verified mutually exclusive

# Problem originating from this function!!!

for mes in mes_list:
    # For some reason, you cant mutate a set that is part of a list that you iterate
    temp_mes = mes.copy()
    rest_union = union_set.difference(temp_mes)
    for batch in long_set:

        # checks if batch is disjoint from all other mutually exclusive sets & that its not disjoint from current MES
        if batch.isdisjoint(rest_union) and batch.intersection(temp_mes):
            temp_mes.intersection_update(batch)

    partners.append(temp_mes.copy())

partners_final = list()

for partner in partners:
    print(len(partner))
    for element in partner:
        partners_final.append(element)


# --------------------------------------- SUM HEX VALUES AND PRINT DECIMAL VALUE --------------------------------------
ip_lists = list()
ip_hex = ""
dec_sum = 0

for partner in partners_final:
    ip_list = partner.split(".")
    temp_hex = ""

    for ip_nbr in ip_list:
        if len(hex(int(ip_nbr))[2:]) == 1:
            temp_hex = "0" + hex(int(ip_nbr))[2:]
        else:
            temp_hex = hex(int(ip_nbr))[2:]

        ip_hex = ip_hex + temp_hex

    dec_sum = dec_sum + int("0x" + ip_hex, 16)
    ip_hex = ""

print("--------------- Answer --------------")
print(dec_sum)
print("-------------------------------------")
