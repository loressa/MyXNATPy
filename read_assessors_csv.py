#!/usr/bin/env python

# Script written by Lorena Escudero (Department of Radiology, University of Cambridge)
# to remove given input subject/experiment/scans in an XNAT project
#
# Usage: edit xnathost/project/user and run 'python3 delete_scans.py input.csv'
# Note: User needs to have admin privileges in project for this script to work

import xnat
import os, sys
import getpass
import csv

# ---------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    # 1 - Inputs

    name_assessor = ''
    
    # 2 - Make XNAT session                                                                                                                           
    xnathost   = 'http://10.1.1.19'
    project_id = 'VTT_test'

    user_id    = 'admin'
    pwd        = getpass.getpass("Password for user name : %s = " % user_id)

    output_file_name = 'VTT_assessments_23.9.21.csv'
    
    with open(output_file_name, mode='w') as output_file:
        output_csv = csv.writer(output_file, delimiter=',')
        output_csv.writerow(['Experiment','Reader','Assessment','Quality','comments'])
        
        with xnat.connect(xnathost, user=user_id, password=pwd) as session:

            xnat_project = session.projects[project_id]
            experiments  = xnat_project.experiments
            
            for experiment in experiments:
                current_experiment = xnat_project.experiments[experiment]
                experiment_label = current_experiment.label
                
                assessors = current_experiment.assessors
                for assessor in assessors:
                    current_assessor = current_experiment.assessors[assessor]

                    if ('RAPID' in current_assessor.label):
                        reader = current_assessor.reader
                        assessment = current_assessor.assessment
                        quality = current_assessor.quality
                        comments = current_assessor.comments
                        
                        output_csv.writerow([experiment_label,reader,assessment,quality,comments])





        #experiments = connection.experiments

        # first make a map with image_session_id and image_session_label
        #dict_image_session_id = {}
        
        #for experiment in experiments:
        #    current_experiment = connection.experiments[experiment]

             #if ('RAPID' in current_experiment.label):
                
        
        #for experiment in experiments:
        #    current_experiment = connection.experiments[experiment]
            
        #    if ('RAPID' in current_experiment.label):
                #print(current_experiment)
        #        image_session_id = current_experiment.image_session_id
        #        reader = current_experiment.reader
        #        assessment = current_experiment.assessment
        #        quality = current_experiment.quality
        #        comments = current_experiment.comments
                
        
