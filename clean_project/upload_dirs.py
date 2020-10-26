#!/usr/bin/env python

# Script written by Lorena Escudero (Department of Radiology, University of Cambridge)
# to upload a clean set of directories to a new XNAT project
# October 2020, v1
# Usage: Edit xnathost, project_id, user_id and then: python3 upload_dirs.py input_dirs_batch0.txt

import xnat
import os
import getpass

import pydicom
import sys

# ------------------------------------------
# Function to upload a directory to XNAT

def upload_scans_dir(session, project_id, subject_id, experiment_id, scans_dir):
    xnat_project = session.projects[project_id]
    # We create the subject with the following line:
    xnat_subject = session.classes.SubjectData(parent=xnat_project, label=subject_id)
    # And now we upload with the import_ method - the experiment will be created in this step
    session.services.import_dir(scans_dir,overwrite='delete', quarantine=False, destination='/archive', trigger_pipelines=None,project=project_id, subject=subject_id, experiment=experiment_id)

# ------------------------------------------

if __name__ == '__main__':

    arguments  = sys.argv[1:]
    input_list = arguments[0]

    xnathost   = 'XNATURL'
    project_id = 'PROJECTID'
    user_id    = 'USERID'
    
    pwd        = getpass.getpass("Password for user name : %s = " % user_id)

    with open(input_list, mode='r') as input_file:
        with xnat.connect(xnathost, user=user_id, password=pwd) as session:
            line = input_file.readline()

            while line:    
                input_dir = line.strip()
                
                input_dicom = input_dir + os.sep + os.listdir(input_dir)[0]
                #print(input_dicom)
                metadata = pydicom.dcmread(input_dicom)
                subject_id = metadata.PatientID
                #experiment_id = subject_id + '_' + metadata.StudyDate
                experiment_id = input_dir.split('/')[5] # ATTN: This is project specific 
                
                print('Uploading subject %s' %subject_id)
                print('          experiment %s' %experiment_id)
                upload_scans_dir(session, project_id, subject_id, experiment_id, input_dir)
                
                line = input_file.readline()
