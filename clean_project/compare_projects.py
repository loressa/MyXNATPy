#!/usr/bin/env python

# Script written by Lorena Escudero (Department of Radiology, University of Cambridge)
# to compare two projects. Special handling of dates changed wrt a reference value
# December 2020, v2
#
# Usage: python3 compare_projects.py [input_reference_dates.csv input_list_subjects.txt]
#
# optional: input_reference_dates.csv if check_dates is True this is needed for ref values
# optional: input_list_subjects.txt if want to check some subjects only, not the whole project


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

# -------------------------------------------------------------
# Function to check the number of scans that are uploaded

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

# -------------------------------------------------------------
# Function to check the number of files that are uploaded

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

# -------------------------------------------------------------
# Function to get the tags of dicom files

def get_dicom_tags(session, project_id, subject_name, experiment_name, scan_name, i):
    #print('Get DICOM tags %s/%s/%s' %(subject_name, experiment_name, scan_name))
    xnat_project    = session.projects[project_id]
    xnat_experiment = xnat_project.subjects[subject_name].experiments[experiment_name]
    xnat_scan       = xnat_experiment.scans[scan_name]

    dicom_file = xnat_scan.resources['DICOM'].files[i]
    with dicom_file.open() as dicomfile:
        metadata = pydicom.dcmread(dicomfile)

    return metadata

# ------------------------------------------
# Function to compare tags

def compare_metadata(date_offset, metadata1, metadata2):
    dict1 = {}
    dict2 = {}

    for key in metadata1:
        dict1[key.description()] = key.value

    for key in metadata2:
        dict2[key.description()] = key.value

    # See TODO below
    if (dict1['SOP Instance UID'] != dict2['SOP Instance UID']):
        print ('*** ATTN! Check order of the files in the scan!!!')
        return None
        
    for key in metadata1:
        try:
            value1 = dict1[key.description()]
            value2 = dict2[key.description()]

            if (('Overlay' in key.description()) and (value1 != value2)):
                print ('ATTN! Check Overlay key %s with values %s and %s' %(key.description(), value1, value2))
            if (('Pixel Data' == key.description()) and (value1 != value2)):
                print ('ATTN! Check Pixel data!!!')

            if (check_dates and (('Date' in key.description()) or ('Time' in key.description()))):
                if ((value1 == value2) and (value1 != '')):
                    print ('ATTN! The tag %s has the same value!' %(key.description()))
                if (value1 != value2):
                    if ('DateTime' in key.description()):
                        date1 = value1[:8]
                        date2 = value2.split('.')[0]
                        date2 = date2[:8]
                        time1 = value1[-6:]
                        compare_dates(date_offset, date1, date2)
                        if (time1 != "000000"):
                            print ('%s: %s vs %s' %(key.description(), value1, value2))
                    elif ('Date' in key.description()):
                        #print ('The tag %s has different values: %s vs %s' %(key.description(), value1, value2))
                        compare_dates(date_offset, value1, value2)
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

# --------------------------------------------------------------------------------
# Function to compare dates: one has changed with respect to the other via offset

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
# Function to check DICOM tags

def check_dicom_tags(session, project1, project2, subject_name, experiment_name, xnat_experiment1, input_list, input_dates_list):
    scans = xnat_experiment1[experiment_name].scans
    for scan in scans:
        print ('*** Checking tags for %s/%s/%s' %(subject_name,experiment_name,scan))
        n_files = len(xnat_experiment1[experiment_name].scans[scan].resources['DICOM'].files)
        # TODO - a couple of cases might have different order of the dicom files between experiments
        for i in range(n_files):
            metadata1 = get_dicom_tags(session, project1, subject_name, experiment_name, scan, i)
            metadata2 = get_dicom_tags(session, project2, subject_name, experiment_name, scan, i)

            #ATTN in case the files are not in the same order in both experiments
            sop1 = metadata1['SOPInstanceUID'].value
            sop2 = metadata2['SOPInstanceUID'].value

            if (sop1 != sop2):
                #print ('different SOP %s and %s' %(metadata1['SOPInstanceUID'], metadata2['SOPInstanceUID']))
                for j in range(n_files):
                    new_metadata2 = get_dicom_tags(session, project2, subject_name, experiment_name, scan, j)
                    new_sop2 = new_metadata2['SOPInstanceUID'].value
                    if (sop1 == new_sop2):
                        sop2 = new_sop2
                        metadata2 = new_metadata2

            # ATTN date_offset is hard-coded here, TODO make it an argument
            date_offset = date(1800,1,1)
            if (check_dates and input_dates_list):
                #input_list  = 'COVID_AdmissionDate_batch1.csv'
                dates_dict  = read_input_dates(input_dates_list)
                try:
                    date_offset = dates_dict[subject_name]
                except:
                    print ('Not found admission date for subject %s' %subject_name)

            compare_metadata(date_offset, metadata1,metadata2)

# ------------------------------------------

if __name__ == '__main__':

    # 1 - Read the input:
    input_list = None
    input_dates_list = None

    arguments   = sys.argv[1:]
    if (len(arguments)>0):
        input_dates_list = arguments[0]

    if (len(arguments)>1):
        input_list  = arguments[1]

    print('Input list: %s'%input_list)
    print('Input dates list: %s'%input_dates_list)

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

        if (input_list):
            subject_list = []
            with open(input_list, 'r') as fp:
                line = fp.readline()
                while line:
                    subject_list.append(line.strip())
                    line = fp.readline()
        else:
            subject_list = subjects1

        # Start with subjects in first project, to check only uploaded so far
        for subject_id in subject_list:
            try:
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
                                    check_dicom_tags(session, project1, project2, subject_name, experiment_name, xnat_experiment1, input_list, input_dates_list)

                        else:
                            experiment = xnat_project2.subjects[subject_name].experiments[experiment_name]
                            print ('ATTN! Not found experiment %s (%s)' %(experiment_name, experiment.data['modality']))
                else:
                    print ('ATTN! Not found subject %s' %subject_name)
            except:
                print ('ATTN! Subject not uploaded %s' %subject_id)

