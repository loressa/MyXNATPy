#!/usr/bin/env python

# Script written by Lorena Escudero (Department of Radiology, University of Cambridge) - June 2020 
# to compare the number of files in a local path (or USB) to the ones uploaded to an XNAT project 
#
# Usage: edit xnathost/project/user and give the input path from where the images have been copied
#

import xnat
import os
import getpass
import pydicom
import fnmatch

def check_dicom_uploaded(session, project_id, subject_id, experiment_id):
    xnat_project = session.projects[project_id]
    # Select the subject and experiment
    xnat_experiment = xnat_project.subjects[subject_id].experiments[experiment_id]
    # And loop over the scans
    scans = xnat_experiment.scans
    n_files = 0 
    for scan in scans:
        n_files = n_files + len(xnat_experiment.scans[scan].resources['DICOM'].files)
        
    return n_files    
 
# ---------------------------------------------------------------------------------------------------------------------   

if __name__ == '__main__':

    xnathost   = 'XNATURL'
    project_id = 'PROJECT'
    
    user_id    = 'USER'
    pwd        = getpass.getpass("Password for user name : %s = " % user_id)
    
    input_path = '/local/path/to/files/'
    
    subjects = []
    for filename in os.listdir(input_path):
        if (os.path.isdir(os.path.join(input_path,filename))): 
            subjects.append(filename)
            
    with xnat.connect(xnathost, user=user_id, password=pwd) as session:
    
        for subject in subjects:
            print('**************')
            print('Subject = %s' %(subject))
            
            # Each subdirectory is a different session or study 
            subject_path = input_path + os.sep + subject
            studies = os.listdir(subject_path)
            
            for study in studies:
                print('  *** Study = %s' %(study))
                study_path = subject_path + os.sep + study 
                n_dicom = 0 
                dicom_file = ''
                dicom_path = '' 
                
                for dirpaths, dirnames, filenames in os.walk(study_path):                
                    for filename in filenames: 
                        if(filename.endswith(".dcm")):
                            n_dicom = n_dicom + 1 
                            dicom_file = os.path.join(dirpaths, filename)
                            dicom_path = dirpaths
                
                metadata      = pydicom.dcmread(dicom_file)
                #experiment_id = metadata.PatientID
                experiment_id = metadata.PatientID + '_' + metadata.StudyDate
                subject_id    = metadata.PatientID
                
                print('     - Comparing Patient ID %s' %(experiment_id))
                if (n_dicom < 1):
                    print('ATTN!!! - check %s' %(study_path))
                else:
                    print('   - Contains %d files' %(n_dicom))
                
                try:
                    n_uploaded = check_dicom_uploaded(session, project_id, subject_id, experiment_id)
                except:
                    print('Not found subject %s + experiment %s in XNAT' %(subject_id, experiment_id))
                    n_uploaded = 0
                    
                print('   - Uploaded %d files' %(n_uploaded))
                print('        - Difference %d ' %(n_dicom-n_uploaded))
                if (n_dicom != n_uploaded):
                    print ('ATTN!!! - check %s' %(study_path))
                        
