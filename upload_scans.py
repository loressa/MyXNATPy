#!/usr/bin/env python

# Script written by Lorena Escudero (Department of Radiology, University of Cambridge) 
# to upload in batch .zip files containing scans - April 2020 
#
# Usage: edit xnathost/project/user and give as input a .txt file containing a line per patient+session
# in the form  'subject_id:session_id:/path/to/scans.zip' 
#
# Based on xnatpy/examples/upload_data.py

import xnat
import os
import getpass

def upload_scans(session, project_id, subject_id, experiment_id, scans_file):
    xnat_project = session.projects[project_id]
    # We create the subject with the following line: 
    xnat_subject = session.classes.SubjectData(parent=xnat_project, label=subject_id)
    # And now we upload with the import_ method - the experiment will be created in this step
    session.services.import_(scans_file,overwrite=None, quarantine=False, destination='/archive', trigger_pipelines=None,project=project_id, subject=subject_id, experiment=experiment_id, content_type=None)
 
# ---------------------------------------------------------------------------------------------------------------------   

if __name__ == '__main__':

    input_list = 'test_file.txt'

    xnathost   = 'XNATURL'
    project_id = 'PROJECT'
    
    user_id    = 'USER'
    pwd        = getpass.getpass("Password for user name : %s = " % user_id)
    
    with xnat.connect(xnathost, user=user_id, password=pwd) as session:
    
        with open(input_list, 'r') as fp:
            line = fp.readline()
        
            while line:
                line          = line.strip()
                subject_id    = line.split(':')[0]
                experiment_id = line.split(':')[1]
                scans_file    = line.split(':')[2]
       
                upload_scans(session, project_id, subject_id, experiment_id, scans_file)
                    
                line = fp.readline()


