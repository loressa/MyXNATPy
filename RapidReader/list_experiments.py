#!/usr/bin/env python

# Script written by Lorena Escudero (Department of Radiology, University of Cambridge)
# To list the experiments available in a given XNAT project, filtering with a keyword

# Usage: Edit information below (xnathost, project_id_list, user_id, keyword) and run python3 list_experiments.py

import xnat
import os
import getpass
import pydicom as pydcm

import csv

# ---------------------------------------------------------------------------------------------------------------------   

def list_experiments(connection, project_id, keyword, output_csv):
    project     = connection.projects[project_id]
    subjects    = project.subjects
    for subject in subjects:
        subject_name = project.subjects[subject].label

        experiments = project.subjects[subject].experiments
        for experiment in experiments:
            experiment_name = project.subjects[subject].experiments[experiment].label
            if (keyword in experiment_name):
                output_csv.writerow([experiment])


# ---------------------------------------------------------------------------------------------------------------------   

if __name__ == '__main__':

    xnathost   = 'XNATURL'
    project_id_list = ['PROJECTID']
    keyword    = 'KEYWORD'
    user_id    = 'USERID'
    pwd        = getpass.getpass("Password for user name : %s = " % user_id)
        
    with xnat.connect(xnathost, user=user_id, password=pwd) as connection:
        for project_id in project_id_list:
            print(project_id)
            output_file_name = 'list_experiments_'+ str(project_id) + '_' + keyword + '.csv'

            with open(output_file_name, mode='w') as output_file:
                output_csv = csv.writer(output_file, delimiter=',')
                output_csv.writerow(['Experiment'])
                
                list_experiments(connection, project_id, keyword, output_csv)
        
