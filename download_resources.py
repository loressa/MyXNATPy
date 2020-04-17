#!/usr/bin/env python

# Script written by Lorena Escudero (Department of Radiology, University of Cambridge) 
# to download scans from XNAT - April 2020 
#
# Usage: edit xnathost/project/user/output_dir and just run normally: python3 download_resources.py 
# Note: This downloads all resources in RAW directories, to download only a list of them, create a list or filter and modify this script
#
# Based on examples in xnatpy/examples

import xnat
import os
import getpass

# ---------------------------------------------------------------------------------------------------------------------   

def dowload_all_scans(connection, project_id, output_dir):
    project     = connection.projects[project_id]
    experiments = project.experiments
    
    for experiment in experiments:
        output = output_dir + project.experiments[experiment].label + '_raw.zip'
        project.experiments[experiment].resources['RAW'].download(output)
    

# ---------------------------------------------------------------------------------------------------------------------   

if __name__ == '__main__':

    xnathost   = 'XNATURL'
    project_id = 'PROJECT'
    
    user_id    = 'USER'
    pwd        = getpass.getpass("Password for user name : %s = " % user_id)
    
    output_dir = 'OUTPUT'
    
    with xnat.connect(xnathost, user=user_id, password=pwd) as connection:
        dowload_all_scans(connection, project_id, output_dir)
        
