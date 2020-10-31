#!/usr/bin/env python

# Script written by Lorena Escudero (Department of Radiology, University of Cambridge)
# to compare two projects. Special handling of dates changed wrt a reference value
# October 2020, v1
# Usage: python3 compare_projects.py input_reference_dates.csv

import xnat

import os, sys
import getpass
import csv

import pydicom

import datetime
from datetime import date, datetime, time

# ------------------------------------------

check_tags  = True
check_dates = True

# -----------------------------------------------------------------------------------------------
# Function to read the input file with PatientID, Admission date as a dictionary

def read_input_dates(input_list):

    dates_dict = {}
    with open(input_list, mode='r') as input_file:
        reader = csv.reader(input_file)
        for row in reader:
            patientID = row[0]
            ad_date   = row[1]
            dates_dict[patientID] = ad_date

    return dates_dict

# ------------------------------------------
# Function to check the number of scans uploaded - unused 

def check_scans_uploaded(session, project_id, subject_id, experiment_id):
    xnat_project = session.projects[project_id]

    # Select the subject and experiment
    xnat_experiment = xnat_project.subjects[subject_id].experiments[experiment_id]

    # And loop over the scans
    scans = xnat_experiment.scans
    n_scans = 0
    for scan in scans:
        n_scans = n_scans + 1 

    return n_scans

# ------------------------------------------
# Function to check the number of dicom files uploaded

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

# ------------------------------------------
# Function that returns the dicom tags of one file, read through pydicom

def get_dicom_tags(session, project_id, subject_name, experiment_name, scan_name, i):
    xnat_project    = session.projects[project_id]
    xnat_experiment = xnat_project.subjects[subject_name].experiments[experiment_name]
    xnat_scan       = xnat_experiment.scans[scan_name]

    dicom_file = xnat_scan.resources['DICOM'].files[i]
    with dicom_file.open() as dicomfile:
        metadata = pydicom.dcmread(dicomfile)

    return metadata

# ------------------------------------------
# Function to compare dicom tags

def compare_metadata(date_offset, metadata1, metadata2):
    dict1 = {}
    dict2 = {}

    for key in metadata1:
        dict1[key.description()] = key.value

    for key in metadata2:
        dict2[key.description()] = key.value

    # Note: This below should not happen anymore    
    if (dict1['SOP Instance UID'] != dict2['SOP Instance UID']):
        print ('*** ATTN! Check order of the files in the scan!!!')
        return None
        
    for key in metadata1:
        try:
            value1 = dict1[key.description()]
            value2 = dict2[key.description()]

            # Special attention to overlays and pixel data
            if (('Overlay' in key.description()) and (value1 != value2)):
                print ('ATTN! Check Overlay key %s with values %s and %s' %(key.description(), value1, value2))
            if (('Pixel Data' == key.description()) and (value1 != value2)):
                print ('ATTN! Check Pixel data!!!')

            # For tags with Date or Time     
            if (check_dates and (('Date' in key.description()) or ('Time' in key.description()))):
                if ((value1 == value2) and (value1 != '')):
                    print ('ATTN! The tag %s has the same value!' %(key.description()))
                if (value1 != value2):
                    # DateTime needs special handling
                    if ('DateTime' in key.description()):
                        date1 = value1[:8]
                        date2 = value2.split('.')[0]
                        date2 = date2[:8]
                        time1 = value1[-6:]
                        compare_dates(date_offset, date1, date2)
                        if (time1 != "000000"):
                            print ('%s: %s vs %s' %(key.description(), value1, value2))

                    # For Date ones, compare with admision date        
                    elif ('Date' in key.description()):
                        compare_dates(date_offset, value1, value2)

                    # For Time ones, just check the they are zero     
                    elif ('Time' in key.description()):
                        if (value1 != "000000.000000"):
                            print ('ATTN! The tag %s is a non-zero time' %(key.description()))
            else:
                if (value1 != value2):
                    print ('The tag %s has different values: %s vs %s' %(key.description(), value1, value2))
        except:
            print ('Not found %s in the second file' %(key.description()))

    for key in metadata2:
        try:
            value1 = dict1[key.description()]
            value2 = dict2[key.description()]
        except:
            print ('Not found %s in the first file' %(key.description()))

# ------------------------------------------
# Function to check the changes performed in dates

def compare_dates(date_offset, value1, value2):
    fix_date      = date(1800,1,1)
    adm_date      = date(int(date_offset[:4]),int(date_offset[5:7]),int(date_offset[-2:]))
    changed_date  = date(int(value1[:4]),int(value1[4:6]),int(value1[-2:]))
    original_date = date(int(value2[:4]),int(value2[4:6]),int(value2[-2:]))
    
    delta     = changed_date - fix_date
    delta2    = original_date - adm_date

    scan_date = adm_date + delta
    
    if (scan_date != original_date):
        print ('ATTN! There is a difference in scan dates of %s' %(original_date - scan_date))


# ------------------------------------------

if __name__ == '__main__':

    # Read the input_list with the admission dates used as reference
    arguments   = sys.argv[1:]
    input_list  = arguments[0]
    
    xnathost   = 'XNATURL'
    user_id    = 'USERID'
    pwd        = getpass.getpass("Password for user name : %s = " % user_id)
    
    project1   = 'PROJECT1'
    project2   = 'PROJECT2'

    with xnat.connect(xnathost, user=user_id, password=pwd) as session:
        xnat_project1 = session.projects[project1]
        xnat_project2 = session.projects[project2]
        subjects1     = xnat_project1.subjects
        subjects2     = xnat_project2.subjects

        # Start with subjects in first project, to check only uploaded so far
        for subject_id in subjects1:
            subject_name = xnat_project1.subjects[subject_id].data['label']
            if (subject_name in subjects2):
                xnat_experiment1 = xnat_project1.subjects[subject_name].experiments
                xnat_experiment2 = xnat_project2.subjects[subject_name].experiments

                # ATTN: Compare experiments from the second, containing all 
                for experiment_id in xnat_experiment2:
                    experiment_name = xnat_project2.subjects[subject_name].experiments[experiment_id].data['label']
                    if (experiment_name in xnat_experiment1):
                        n_files2 = check_dicom_uploaded(session, project2, subject_name, experiment_name)
                        n_files1 = check_dicom_uploaded(session, project1, subject_name, experiment_name)
                        if (n_files1 != n_files2):
                            print ('ATTN: %s dicom in first project and %s in second (experiment: %s)' %(n_files1, n_files2, experiment_name))
                        else:
                            if (check_tags):
                                scans = xnat_experiment1[experiment_name].scans
                                for scan in scans:
                                    print ('*** Checking tags for %s/%s/%s' %(subject_name,experiment_name,scan))
                                    n_files = len(xnat_experiment1[experiment_name].scans[scan].resources['DICOM'].files)

                                    for i in range(n_files):
                                        metadata1 = get_dicom_tags(session, project1, subject_name, experiment_name, scan, i)
                                        metadata2 = get_dicom_tags(session, project2, subject_name, experiment_name, scan, i)

                                        #ATTN in case the files are not in the same order in both experiments
                                        sop1 = metadata1['SOPInstanceUID'].value
                                        sop2 = metadata2['SOPInstanceUID'].value
                                        
                                        if (sop1 != sop2):
                                            for j in range(n_files):
                                                new_metadata2 = get_dicom_tags(session, project2, subject_name, experiment_name, scan, j)
                                                new_sop2 = new_metadata2['SOPInstanceUID'].value
                                                if (sop1 == new_sop2):
                                                    sop2 = new_sop2
                                                    metadata2 = new_metadata2

                                        # ATTN date_offset is hard-coded here, TODO make it an argument             
                                        date_offset = date(1800,1,1)
                                        if (check_dates):
                                            dates_dict  = read_input_dates(input_list)
                                            try:
                                                date_offset = dates_dict[subject_name]
                                            except:
                                                print ('Not found admission date for subject %s' %subject_name)
                                                
                                        compare_metadata(date_offset, metadata1,metadata2)
                    else:
                        experiment = xnat_project2.subjects[subject_name].experiments[experiment_name]
                        print ('ATTN! Not found experiment %s (%s)' %(experiment_name, experiment.data['modality']))
            else:
                print ('ATTN! Not found subject %s' %subject_name)

