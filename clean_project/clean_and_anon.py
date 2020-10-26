#!/usr/bin/env python

# Script written by Lorena Escudero (Department of Radiology, University of Cambridge)
# to avoid certain image types and clean some specific DICOM tags
# October 2020, v1 
# Usage: Edit input and output_path, then: python3 clean_and_anon.py input_file.txt > list_commands.sh

import sys, os, glob
import pydicom

# -----------------------------------------------------------------------------------------------
# Function to check the DICOM tag ImageType, targetting certain keywords

def check_file_type(dicom_file):
    try:
        data = pydicom.dcmread(dicom_file)
        # Check ImageType[0]
        try:
            image_type_0 = data.ImageType[0].lower()
            if (('aqnetsc' in image_type_0) or ('protocol' in  image_type_0) or ('screen' in image_type_0) or ('presentation' in image_type_0) or ('report' in image_type_0) or ('exam' in image_type_0)):
                return False
        except:
            print ('ATTN: No ImageType in %s ' %dicom_file)
            return False
        # Check ImageType[1]
        try:
            image_type_1 = data.ImageType[1].lower()
            if (('aqnetsc' in image_type_1) or ('protocol' in  image_type_1) or ('screen' in image_type_1) or ('presentation' in image_type_1) or ('report' in image_type_1) or ('exam' in image_type_1)):
                return False
        except:
            print ('ATTN: No second ImageType in %s ' %dicom_file)
        # Check ImageType[2]    
        try:
            image_type_2 = data.ImageType[2].lower()
            if (('aqnetsc' in image_type_2) or ('protocol' in  image_type_2) or ('screen' in image_type_2) or ('presentation' in image_type_2) or ('report' in image_type_2) or ('exam' in image_type_2)):
                return False
        except:
            print ('ATTN: No third ImageType in %s ' %dicom_file)
    except:
        print ('ATT: No metadata in %s ' %dicom_file)
        return False
    
    return True

# -----------------------------------------------------------------------------------------------

if __name__ == '__main__':

    arguments   = sys.argv[1:]
    input_list  = arguments[0]
    input_path  = '/path/to/input/dir/'
    output_path = '/path/to/output/dir/'
    
    with open(input_list, 'r') as fp:
        line = fp.readline()
        while line:
            output_session = output_path + os.sep + line.strip()
            try:
                os.mkdir(output_session)
            except:
                pass

            # Follow the structure of the XNAT filesystem
            scan_path = input_path + os.sep + line.strip() + os.sep + 'SCANS'
            scans = os.listdir(scan_path)
            for scan in scans:
                try: 
                    files = os.listdir(scan_path + os.sep + scan + "/DICOM/")
                    for file in files:
                        if (not file.endswith(".xml")):
                            input_file  = scan_path + os.sep + scan + "/DICOM/" + file
                            output_file = output_session + os.sep + file

                            # Print the command using DicomRemap
                            if check_file_type(input_file):
                                print('/home/ubuntu/DicomBrowser-1.7.0b4/bin/DicomRemap -d clean.das -o %s %s' %(output_session, input_file))
                except:
                    print('ATTN: No DICOM in session %s, scan %s' %(line.strip(),scan))

            line = fp.readline()
                            
