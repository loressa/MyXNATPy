#!/usr/bin/env python

# Script written by Lorena Escudero (Department of Radiology, University of Cambridge)
# to create and populate a Rapid Reader worklist per user in a given list of users

# Usage: edit xnathost, project_id, user_id, list_readers adn due_date, then python3 make_worklist.py
# NOTE: this is an example done for a specific use case, with a VTT template, change accordingly 

import os

import xnat
import getpass

xnathost   = 'XNATURL'
project_id = 'PROJECTID'
user_id    = 'USERID'
pwd        = getpass.getpass("Password for user name : %s = " % user_id)

list_readers = ['READER']
due_date = '1640995199000' #31st december 2021

for reader in list_readers:
    print('******************')
    print(' Reader %s' %reader)
    # 1 - curl command to create the worklist
    command_create = 'curl -u ' + user_id + ':' + pwd + ' -X POST ' + xnathost + 'xapi/workLists/ -H \'Content-Type: application/json\' -d \'{\"readerUsername\":\"' + reader \
                    + '\",\"dueDate\": ' + due_date + ',\"name\":\"VTT\",\"description\":\"Visual Turing Test\", \"reportId\":\"VTT\", \"status\":\"Open\"}\''
    #print(command_create)

    # 2 - execute and store the worklist_id created
    result = os.popen(command_create).read()
    #print(result)
    worklist_id = result.split('id')[1]
    worklist_id = worklist_id.split(',')[0]
    worklist_id = worklist_id.replace("\"", "")
    worklist_id = worklist_id.replace(":", "")
    print('Worklist ID: %s' %worklist_id)

    # 3 - read the list of items for this user
    list_experiments = '/Users/les44/Documents/RadiologyResearch/VTT/Worklists/' + reader + '.txt'

    # 4 - populate the worklist
    with open(list_experiments, 'r') as fp:
        line = fp.readline()

        while (line):
            experiment_id = line.strip()
            command_item = 'curl -u ' + user_id + ':' + pwd + ' -X POST ' + xnathost + 'xapi/workLists/' + worklist_id + \
                       '/items -H \'Content-Type: application/json\' -d \'{\"experimentId\":\"' + experiment_id + '\"}\''
            #print(command_item)
            os.system(command_item)
            line = fp.readline()

