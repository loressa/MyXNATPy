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
        #print(subject_name)
        experiments = project.subjects[subject].experiments
        if (len(experiments)==0):
            output_csv.writerow([subject_name, '-', '-', 0])
        for experiment in experiments:
            #print(experiment)
            n_total = 0 
            experiment_name = project.subjects[subject].experiments[experiment].label
            scans = project.subjects[subject].experiments[experiment].scans
            for scan in scans:
                #print(scan)
                try:
                    n_files = len(project.subjects[subject].experiments[experiment].scans[scan].resources['DICOM'].files)
                except:
                    n_files = 0
                n_total = n_total + n_files
                output_csv.writerow([subject_name, experiment_name, scan, n_files])
            output_csv.writerow([subject_name, experiment_name, 'All', n_total])
                

# ---------------------------------------------------------------------------------------------------------------------   

if __name__ == '__main__':

    xnathost   = ''
    project_id_list = ['']
    user_id    = ''
    pwd        = ''
        
    with xnat.connect(xnathost, user=user_id, password=pwd) as connection:
        for project_id in project_id_list:
            print(project_id)
            output_file_name = 'project_stats_'+ str(project_id) + '.csv'

            with open(output_file_name, mode='w') as output_file:
                output_csv = csv.writer(output_file, delimiter=',')
                output_csv.writerow(['Subject', 'Session', 'Scan', 'Nfiles'])
                
                list_subjects_experiments(connection, project_id, output_csv)
        
