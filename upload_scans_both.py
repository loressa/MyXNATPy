#!/usr/bin/env python

# Script written by Lorena Escudero (Department of Radiology, University of Cambridge) 
# to upload in batch scans to XNAT - November 2020
#
# Usage: edit xnathost/project/user and give as input a .csv file containing per row: file_path,subject,session
# to run: python3 upload_scans_both.py input_list.csv
#
# Based on xnatpy/examples/upload_data.py

import xnat
import os, sys
import getpass

from csv import reader

# ---------------------------------------------------------------------------------------------------------------------

def upload_scans_zip(session, project_id, subject_id, experiment_id, scans_file):
    xnat_project = session.projects[project_id]
    # We create the subject with the following line:
    xnat_subject = session.classes.SubjectData(parent=xnat_project, label=subject_id)
    # And now we upload with the import_ method - the experiment will be created in this step
    session.services.import_(scans_file,overwrite=None, quarantine=False, destination='/archive', trigger_pipelines=None,project=project_id, subject=subject_id, experiment=experiment_id, content_type=None)

# ---------------------------------------------------------------------------------------------------------------------

def upload_scans_dir(session, project_id, subject_id, experiment_id, scans_dir):
    xnat_project = session.projects[project_id]
    # We create the subject with the following line:
    xnat_subject = session.classes.SubjectData(parent=xnat_project, label=subject_id)
    # And now we upload with the import_ method - the experiment will be created in this step
    session.services.import_dir(scans_dir,overwrite=None, quarantine=False, destination='/archive', trigger_pipelines=None,project=project_id, subject=subject_id, experiment=experiment_id)

# ---------------------------------------------------------------------------------------------------------------------   

if __name__ == '__main__':

    arguments  = sys.argv[1:]
    input_list = arguments[0]

    xnathost   = 'XNATURL'
    project_id = 'PROJECTID'
    
    user_id    = 'USERID'
    pwd        = getpass.getpass("Password for user name : %s = " % user_id)
    
    with xnat.connect(xnathost, user=user_id, password=pwd) as session:

        with open(input_list, 'r') as fp:
            csv_reader = reader(fp)

            for row in csv_reader: 
                scans_file    = row[0]
                subject_id    = row[1]
                experiment_id = row[2]

                print ('Uploading to subject %s and experiment %s files from %s' %(subject_id, experiment_id, scans_file))

                #Note: choose one of the two options below, depending if input file has a list of .zip or of directories
                #upload_scans_zip(session, project_id, subject_id, experiment_id, scans_file)
                upload_scans_dir(session, project_id, subject_id, experiment_id, scans_file)
