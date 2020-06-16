#!/usr/bin/env python

# Script written by Lorena Escudero (Department of Radiology, University of Cambridge) 
# to remove all subjects in an XNAT project - June 2020 
#
# Usage: edit xnathost/project/user and run 'python3 remove_subjects.py'
# Note: This removes all subjects, can be modified to remove only some from an input list 
# Note: User needs to have admin privileges in project for this script to work  
#

import xnat
import os
import getpass

def remove_subjects(session, project_id):
    xnat_project = session.projects[project_id]
    # We find all subjects:
    subjects = xnat_project.subjects
    for subject_id in subjects:
        print('Removing subject %s' %(subject_id))
        subject = xnat_project.subjects[subject_id]
        subject.delete()
    
# ---------------------------------------------------------------------------------------------------------------------   

if __name__ == '__main__':

    xnathost   = 'XNATURL'
    project_id = 'PROJECT'
    
    user_id    = 'USER'
    pwd        = getpass.getpass("Password for user name : %s = " % user_id)
    
    #input_list = '/path/to/input_list'

    with xnat.connect(xnathost, user=user_id, password=pwd) as session:
        remove_subjects(session, project_id)

