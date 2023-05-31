import os
import sys
import pprint
import re
from datetime import datetime


def compute_access_pattern(data_path,delta_time):

    timestamp_format = "%d/%b/%Y:%H:%M:%S %z"
    timestamp_pattern = r'\[(.*?)\]'

    normal_access_sequences={}

    for file_path in os.listdir(data_path):

        if file_path == 'ip_list':
            continue
        ip_address = file_path
        file_path = '{}/{}'.format(data_path, file_path)

        f = open(file_path,'r')
        lines = f.readlines()

        t0=''
        t1=''
        access_sequence = []


        for line in lines:


            # first line
            if t0=='':
                t0=line

            t1 = line

            match = re.search(timestamp_pattern, t0)
            timestamp1=match.group(1)

            match = re.search(timestamp_pattern, t1)
            timestamp2=match.group(1)

            datetime1 = datetime.strptime(timestamp1, timestamp_format)
            datetime2 = datetime.strptime(timestamp2, timestamp_format)

            time_difference = datetime2 - datetime1

            # if we re inside the working sequence
            if time_difference.total_seconds() <= delta_time:
                #delta_time += time_difference.total_seconds()
                #print(delta_time)

                data = t1.split(' ')
                method = data[5]
                resource = data[6]
                answer = data[8]
                # if the line is regular
                if len(data)>=11:
                    referrer = data[10]
                access_sequence.append("{} {} {} {} {}".format(timestamp2, method, resource, answer,referrer))

            else:
                log_parts = t0.split(' ')
                address= log_parts[0]
                if address in normal_access_sequences.keys():
                    if len(access_sequence) !=0:
                        normal_access_sequences[address].append(access_sequence)

                else:
                    normal_access_sequences[address]=[access_sequence]
                # reset the timer
                #delta_time=0
                # reinitialise the access sequence
                access_sequence = []

            # change the root line
            t0=t1

        # add the last processed sequence
        log_parts = t0.split(' ')
        address= log_parts[0]
        if address in normal_access_sequences.keys():
            if len(access_sequence) !=0:
                normal_access_sequences[address].append(access_sequence)

        else:
            normal_access_sequences[address]=[access_sequence]

    return normal_access_sequences

def analyze_request_sequence(address,access_sequence):
    print(address)
    print(access_sequence)


if __name__=="__main__":

    log_folder_path=sys.argv[1]

    delta_time=sys.argv[2]

    normal_access_sequences = compute_access_pattern(log_folder_path)
    #pprint.pprint(normal_access_sequence)

    for address in normal_access_sequences.keys():
        analyze_request_sequence(address,normal_access_sequences[address])
