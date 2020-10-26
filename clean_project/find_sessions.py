#!/usr/bin/env python

# Script written by Lorena Escudero (Department of Radiology, University of Cambridge)
# to find session labels in XNAT given an input list of subject IDs
# October 2020, v1
# Usage: python3 find_sessions.py input_list.csv

import xnat
import os, sys
import getpass
import csv

# -----------------------------------------------------------------------------------------------
# Function to read the input file with PatientID, Admission date as a dictionary

def read_input_dates(input_list):

    dates_dict = {}
    with open(input_list, mode='r') as input_file:
        reader = csv.reader(input_file)
        for row in reader:
            patientID = row[0]
            ad_date   = row[1]
            dates_dict[patientID] = ad_date

    return dates_dict


# -------------------------------------------------------------------------------------------------------------------
# Function to find sessions associated to a given subject label

def find_sessions(project_id, patient_id):
    
    xnat_project = session.projects[project_id]
    try:
        xnat_subject     = xnat_project.subjects[patient_id]
        xnat_experiments = xnat_subject.experiments
        for experiment_id in xnat_experiments:
            experiment = xnat_subject.experiments[experiment_id]
            if (experiment.data['modality'] != 'CT'): # OPTIONAL
                print(experiment.data['label'])
    except:
        print ('Not found this subject: %s ' %patient_id)
    

# -------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    # 1 - Read the input list of PatientID - Admission date as a dictionary
    arguments   = sys.argv[1:]
    input_list  = arguments[0]
    dates_dict  = read_input_dates(input_list)
    
    # 2 - Make XNAT session         
    xnathost    = 'XNATURL'
    project_id  = 'PROJECTID'
    user_id     = 'USERID'
    
    pwd         = getpass.getpass("Password for user name : %s = " % user_id)

    # 3 - Find sessions for PatientIDs in input and print them out 
    with xnat.connect(xnathost, user=user_id, password=pwd) as session:
        for key in dates_dict:
            #print(key)
            patient_id = key.strip()
            find_sessions(project_id, patient_id)
            
