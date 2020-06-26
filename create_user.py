#!/usr/bin/env python

# Script written by Lorena Escudero (Department of Radiology, University of Cambridge) 
# to create new users in XNAT - June 2020
#
# Usage: edit xnathost/project and give as input a .txt file containing a line per user
# in the form  'user_id:firstName:lastName:email' 
#

import xnat
import os
import getpass

# ---------------------------------------------------------------------------------------------------------------------   

if __name__ == '__main__':

    input_list = 'test_file.txt'

    xnathost   = 'XNATURL'
    project_id = 'PROJECT'
    
    admin      = 'admin'
    pwd        = getpass.getpass("Password for user name : %s = " % user_id)
    
    with xnat.connect(xnathost, user=user_id, password=pwd) as session:
    
        with open(input_list, 'r') as fp:
            line = fp.readline()
        
            while line:
                line          = line.strip()
                xnat_user_id  = line.split(':')[0]
                xnat_user_firstName = line.split(':')[1]
                xnat_user_lastName = line.split(':')[2]
                xnat_user_email = line.split(':')[3]

                xnat_user_json =  { "username"  :   xnat_user_uid, \
                                    "firstName" :   xnat_user_firstName,  \
                                    "lastName"  :   xnat_user_lastName,  \
                                    "email"     :   xnat_user_mail, \
                                    "verified"  :   "true", \
                                    "secured"   :   "true", \
                                    "active"    :   "true", \
                                    "enabled"   :   "true" }
                
                session.post('/xapi/users/', json=xnat_user_json )
                                    
                line = fp.readline()


