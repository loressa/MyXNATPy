#!/usr/bin/env python

# Script written by Lorena Escudero (Department of Radiology, University of Cambridge) 
# to remove given input subject/experiment/scans in an XNAT project 
#
# Usage: edit xnathost/project/user and run 'python3 delete_scans.py input.csv'
# Note: User needs to have admin privileges in project for this script to work  
#

import xnat
import os, sys
import getpass

# ---------------------------------------------------------------------------------------------------------------------   
# Function that removes a single scan in a given subject and experiment in XNAT

def remove_scan(session, project_id, subject_id, experiment_id, scan_id):

    try:
        xnat_project    = session.projects[project_id]
        xnat_subject    = xnat_project.subjects[subject_id]
        xnat_experiment = xnat_subject.experiments[experiment_id]
        xnat_scan       = xnat_experiment.scans[scan_id]

        print ('Deleting scan %s/%s/%s' %(subject_id, experiment_id, scan_id))
        xnat_scan.delete()
        
    except:
        print ('Not found subject %s, experiment %s and scan %s' %(subject_id, experiment_id, scan_id))
    
        
# ---------------------------------------------------------------------------------------------------------------------   

if __name__ == '__main__':

    # 1 - Read the input list of sessions to check
    arguments   = sys.argv[1:]
    input_list  = arguments[0]

    # 2 - Make XNAT session
    xnathost   = 'XNATURL'
    project_id = 'PROJECTID'
    
    user_id    = 'USERID'
    pwd        = getpass.getpass("Password for user name : %s = " % user_id)
    
    with xnat.connect(xnathost, user=user_id, password=pwd) as session:
        with open(input_list, 'r') as fp:
            line    = fp.readline()
            while line:
                line_clean    = line.strip()
                subject_id    = line_clean.split(',')[0]
                experiment_id = line_clean.split(',')[1]
                scan_id       = line_clean.split(',')[2]

                remove_scan(session, project_id, subject_id, experiment_id, scan_id)

                line    = fp.readline()
