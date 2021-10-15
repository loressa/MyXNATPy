#!/usr/bin/env python

# Script written by Lorena Escudero (Department of Radiology, University of Cambridge)
# to read assessors created using the Visual Turing Test VTT plugins
#
# Usage: edit xnathost/project/user and run 'python3 read_assessors_csv.py'


import xnat
import os, sys
import getpass
import csv

# --------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    xnathost   = 'XNATURL'
    project_id = 'PROJECTID'

    user_id    = 'USERID'
    pwd        = getpass.getpass("Password for user name : %s = " % user_id)

    output_file_name = 'OUTPUTFILE.csv'
    
    with open(output_file_name, mode='w') as output_file:
        output_csv = csv.writer(output_file, delimiter=',')
        output_csv.writerow(['Experiment','Reader','Assessment', 'Confidence', 'Quality','comments'])
        
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
                        confidence = current_assessor.confidence
                        quality = current_assessor.quality
                        comments = current_assessor.comments
                        
                        output_csv.writerow([experiment_label,reader,assessment,confidence,quality,comments])                
        
