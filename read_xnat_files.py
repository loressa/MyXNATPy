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

# ---------------------------------------------------------------------------------------------------------------------   

def read_dicom_files(connection, project_id):
    project     = connection.projects[project_id]
    subjects    = project.subjects
    
    for subject in subjects:
        experiments = project.subjects[subject].experiments
        for experiment in experiments:
            scans = project.subjects[subject].experiments[experiment].scans
            for scan in scans:
                n_files = len(project.subjects[subject].experiments[experiment].scans[scan].resources['DICOM'].files)
                for i in range(n_files):
                    file = project.subjects[subject].experiments[experiment].scans[scan].resources['DICOM'].files[i]
                    with file.open() as dicomfile:
                        process_dicom(dicomfile)
    
# ---------------------------------------------------------------------------------------------------------------------   

def process_dicom(input_dicom):
    data = pydcm.dcmread(input_dicom)
    print (data.SliceThickness)

# ---------------------------------------------------------------------------------------------------------------------   

if __name__ == '__main__':

    xnathost   = 'XNATURL'
    project_id = 'PROJECT'
    
    user_id    = 'USER'
    pwd        = getpass.getpass("Password for user name : %s = " % user_id)
        
    with xnat.connect(xnathost, user=user_id, password=pwd) as connection:
        read_dicom_files(connection, project_id)
        
