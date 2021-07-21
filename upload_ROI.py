#!/usr/bin/env python

# Script written by Lorena Escudero (Department of Radiology, University of Cambridge)
# to upload ROIs to XNAT - latest version: July 2021
#                                                                                                                                                                                  
# Usage: edit all information below and just run with python3 upload_ROI.py
# Note: simply using REST API call for ROI collections in XNAT

import xnat
import getpass

# ------------------------------------------
# INPUTS - Please edit 
# ------------------------------------------

xnathost   = 'XNATURL'
user_id    = 'USERID'
pwd        = getpass.getpass("Password for user name : %s = " % user_id)

project_label = 'PROJECTID'
subject_label = 'SUBJECTID'
experiment_label = 'EXPERIMENTID'

file_path = 'FILEPATH'
segmentation_type = 'RTSTRUCT' # either SEG or RTSTRUCT 
segmentation_name = 'NAME' # name the ROI collection will have in XNAT 

# ------------------------------------------
# INPUTS - Open session and upload
# ------------------------------------------

with xnat.connect(xnathost, user=user_id, password=pwd) as session:
    xnat_project = session.projects[project_label]
    xnat_subject = session.classes.SubjectData(parent=xnat_project,label=subject_label)
    xnat_experiment = xnat_subject.experiments[experiment_label]
    target_url = (f"/xapi/roi/projects/{xnat_project.id}/sessions/{xnat_experiment.id}/collections/{segmentation_name}"f"?type={segmentation_type}&overwrite=true")

    with open(file_path, 'rb') as file:
        response = session.put(target_url, data=file, accepted_status=[200])
        print(response)

        
