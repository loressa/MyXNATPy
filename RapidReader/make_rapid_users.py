#!/usr/bin/env python

# Script written by Lorena Escudero (Department of Radiology, University of Cambridge)
# to create users automatically and randomly assigned usernames for a given list of emails

# Usage: edit xnathost and user_id and run python3 make_rapid_users.py
# NOTE: This is an example use case for VTT, change usernames etc accordingly

import os
import getpass
import random

xnathost   = 'XNATURL'
if (xnathost[-1] == '/'):
    xnathost = xnathost[:-1]

user_id    = 'USERID'
pwd        = getpass.getpass("Password for user name : %s = " % user_id)

list_emails = ['EMAIL_ADDRESS']
n_users = len(list_emails)

seed = 15112021
random.seed(seed)
random.shuffle(list_emails)

for i in range(n_users):
    username = 'vtt_user' + str(i+1)
    first_name = 'VTT'
    last_name  = 'USER' + str(i+1)
    print('******************')
    print(' User %s' % username)

    command_create = 'curl -u ' + user_id + ':' + pwd + ' -X POST \"' + xnathost + '/xapi/users\" -H \"accept: application/json\" -H \"Content-Type: application/json\" ' + \
                    ' -d \"{ \\\"email\\\": \\\"' + list_emails[i] + '\\\", \\\"enabled\\\": true, \\\"firstName\\\": \\\"' + first_name + \
                     '\\\", \\\"lastName\\\": \\\"' + last_name + '\\\", \\\"username\\\": \\\"' + username + '\\\", \\\"verified\\\": true}\"'

    #print(command_create)
    os.system(command_create)

    command_rapid = 'curl -u ' + user_id + ':' + pwd + ' -X POST \"' + xnathost + '/xapi/rapidReader/users\"' \
                    ' -H \"accept: application/json\" -H \"Content-Type: application/json\" -d \"{ \\\"username\\\": \\\"' + username +  '\\\"}\"'

    #print(command_rapid)
    os.system(command_rapid)
