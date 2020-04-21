#!/usr/bin/env python

# Script written by Lorena Escudero (Department of Radiology, University of Cambridge) 
# to upload in batch files as resources as well as scans - March 2020 
#
# Usage: edit xnathost/project/user and give as input a .txt file containing a line per patient+session
# in the form  'subject_id:session_id:/path/to/scans.zip:/path/to/resources_file1:/path/to/resources_file2..' 
# Note: Writen for CT session and to store in Resources/RAW
#
# Based on xnatpy/examples/upload_data.py

import xnat
import os
import getpass

# ---------------------------------------------------------------------------------------------------------------------

def upload_scans(session, project_id, subject_id, experiment_id, scans_file):
    xnat_project = session.projects[project_id]
    # We create the subject with the following line: 
    xnat_subject = session.classes.SubjectData(parent=xnat_project, label=subject_id)
    # And now we upload with the import_ method - the experiment will be created in this step
    session.services.import_(scans_file,overwrite=None, quarantine=False, destination='/archive', trigger_pipelines=None,project=project_id, subject=subject_id, experiment=experiment_id, content_type=None)

# ---------------------------------------------------------------------------------------------------------------------

def upload_resources(session, project_id, subject_id, experiment_id, resources):
    xnat_project        = session.projects[project_id]
    xnat_subject        = session.classes.SubjectData(parent=xnat_project, label=subject_id)
    xnat_experiment     = session.classes.CtSessionData(parent=xnat_subject, label=experiment_id)
    # Create the resources folder called 'RAW'
    xnat_resources      = session.classes.ResourceCatalog(parent=xnat_experiment, label='RAW')
    # And upload the resource files there
    for resource_file in resources:
        resources_file_name = resource_file.split(os.sep)[-1]
        print(resources_file_name)
        xnat_resources.upload(resource_file,resources_file_name)
 
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
                resources     = []
                for i in range(3,len(line.split(':'))):
                    resources.append(line.split(':')[i])
       
                upload_scans(session, project_id, subject_id, experiment_id, scans_file)
                upload_resources(session, project_id, subject_id, experiment_id, resources)
                    
                line = fp.readline()


