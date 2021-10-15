#!/usr/bin/env python

# Script written by Lorena Escudero (Department of Radiology, University of Cambridge) 
# to read DICOM files directly from XNAT - April 2020 
#
# Usage: edit xnathost/project/user and just run normally: python3 read_xnat_files.py 
# Note: This reads 'all DICOM files' in a project, for only a set of them, create a list or filter and modify this script
# As an example, it prints to screen the values of the slice thickness of each file 
#
# Based on examples in xnatpy/examples

import xnat
import os
import getpass
import pydicom as pydcm

import csv

# ---------------------------------------------------------------------------------------------------------------------   

def list_subjects_experiments(connection, project_id, output_csv):
    project     = connection.projects[project_id]
    subjects    = project.subjects
    
    for subject in subjects:
        subject_name = project.subjects[subject].label

        experiments = project.subjects[subject].experiments
        for experiment in experiments:
            experiment_name = project.subjects[subject].experiments[experiment].label
            output_csv.writerow([subject_name, experiment_name])


# ---------------------------------------------------------------------------------------------------------------------   

if __name__ == '__main__':

    xnathost   = 'XNATURL'
    project_id_list = ['PROJECTID']
    user_id    = 'USERID'
    pwd        = getpass.getpass("Password for user name : %s = " % user_id)
        
    with xnat.connect(xnathost, user=user_id, password=pwd) as connection:
        for project_id in project_id_list:
            print(project_id)
            output_file_name = 'list_subjects_experiments_'+ str(project_id) + '.csv'

            with open(output_file_name, mode='w') as output_file:
                output_csv = csv.writer(output_file, delimiter=',')
                output_csv.writerow(['Subject', 'Session'])
                
                list_subjects_experiments(connection, project_id, output_csv)
        
