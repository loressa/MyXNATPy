#!/usr/bin/env python

# Script written by Lorena Escudero (Department of Radiology, University of Cambridge)
# to check if a list of sessions has been correctly uploaded to XNAT 
# October 2020, v1
# Usage: python3 check_uploaded_sessions.py input_list.txt

import xnat
import os, sys
import getpass
import csv

# -----------------------------------------------------------------------------------------------
# Function to check if a session exists

def check_session_exists(session, project_id, subject_id, experiment_id):

    xnat_project = session.projects[project_id]
    try:
        xnat_subject = xnat_project.subjects[subject_id]
        try:
            xnat_experiment = xnat_subject.experiments[experiment_id]
            scans   = xnat_experiment.scans
            if (not len(scans) > 0):
                print ('ATTN! Session %s is emnpty' %experiment_id)
        except:
            print ('ATTN! Session %s not found' %experiment_id)
    except:
        print ('ATTN! Subject %s not found' %subject_id)
    

# -----------------------------------------------------------------------------------------------

if __name__ == '__main__':

    # 1 - Read the input list of sessions to check 
    arguments   = sys.argv[1:]
    input_list  = arguments[0]

    # 2 - Make XNAT session
    xnathost    = 'XNATURL'
    project_id  = 'PROJECTID'
    user_id     = 'USERID'

    pwd         = getpass.getpass("Password for user name : %s = " % user_id)

    # 3 - Find sessions for PatientIDs in input and print them out
    with xnat.connect(xnathost, user=user_id, password=pwd) as session:
        with open(input_list, 'r') as fp:
            line    = fp.readline()
            while line:
                experiment_id = line.strip()
                subject_id    = experiment_id.split('_')[0]
                #print(experiment_id)
                
                check_session_exists(session, project_id, subject_id, experiment_id)

                line    = fp.readline()    

    print ('Done!')
