#!/usr/bin/env python

# Script written by Lorena Escudero (Department of Radiology, University of Cambridge)
# to change the date of DICOM files according as related to an input date 
# October 2020, v1
# Usage: Edit input_path, then: python3 change_date.py input_file.csv

import datetime
from datetime import date, datetime, time

import csv
import os, sys
import pydicom

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

# -----------------------------------------------------------------------------------------------

if __name__ == '__main__':

    arguments   = sys.argv[1:]
    input_list  = arguments[0]
    dates_dict  = read_input_dates(input_list)

    # ATTN: Edit this accordingly 
    input_path = '/path/to/input/dir/'

    # loop over all directories in upstream input_path, prepared to contain only .dcm
    for dirpaths, dirnames, filenames in os.walk(input_path):    
        for filename in filenames:
            dicom_file      = os.path.join(dirpaths, filename)
            print(dicom_file)
            metadata        = pydicom.dcmread(dicom_file)
            patient_id      = metadata.PatientID
            input_scan_date = metadata.StudyDate
            input_adm_date  = dates_dict[patient_id]

            #Python datetime.date(year, month, day)
            adm_date  = date(int(input_adm_date[:4]),int(input_adm_date[5:7]),int(input_adm_date[-2:]))
            scan_date = date(int(input_scan_date[:4]),int(input_scan_date[4:6]),int(input_scan_date[-2:]))
            #print(adm_date)
            #print(scan_date)

            fix_start = date(1800,1,1)
            delta     = scan_date - adm_date
            #print(delta)

            corr_date      = fix_start + delta
            corr_date_time = datetime(corr_date.year, corr_date.month, corr_date.day, 0, 0, 0, 0)
            #print(corr_date)

            # change relevant keywords related to scan date in the DICOM tags
            keywords  = metadata.dir('Date')
            for keyword in keywords:
                if ((keyword != 'PatientBirthDate') and (not 'Calibration' in keyword)):

                    if ((keyword != 'AcquisitionDate') and (keyword != 'ContentDate') and (keyword != 'SeriesDate') and (keyword != 'StudyDate')):
                        print ('ATTN changing keyword %s' %keyword)
                        
                    if ('Time' in keyword):
                        metadata[keyword].value = corr_date_time
                    else:     
                        metadata[keyword].value = corr_date

            # change also times to 0
            keywords_time = metadata.dir('Time')
            for keyword in keywords_time:
                if ((not 'Date' in keyword) and (not 'Calibration' in keyword) and (not 'Birth' in keyword) and (not 'Exposure' in keyword) and (not 'Detector' in keyword)):

                    if ((keyword != 'AcquisitionTime') and (keyword != 'ContentTime') and (keyword != 'SeriesTime') and (keyword != 'StudyTime')):
                        print ('ATTN changing keyword %s' %keyword)

                    metadata[keyword].value = "000000.000000"
                
            # finally remove the private tags and save                
            metadata.remove_private_tags()            
            metadata.save_as(dicom_file)            
