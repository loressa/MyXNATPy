#!/usr/bin/env python

# Script written by Lorena Escudero (Department of Radiology, University of Cambridge)
# to remove all private tags using the pydicom method for that 
# January 2021, v1
# Usage: python3 remove_private_tags.py input_file.csv

import csv
import os, sys
import pydicom

# -----------------------------------------------------------------------------------------------

if __name__ == '__main__':

    arguments   = sys.argv[1:]
    if (len(arguments)>0):
        input_list  = arguments[0]
    else:
        print('Error: You need to provide a list of directories. Bye.')
        exit()

    with open(input_list, mode='r') as input_file:
        line = input_file.readline()
        while line:
            input_path = line.strip()
            for dirpaths, dirnames, filenames in os.walk(input_path):
                for filename in filenames:
                    if (not filename.endswith(".xml")):
                        #print(filename)
                        dicom_file      = os.path.join(dirpaths, filename)
                        #print(dicom_file)
                        metadata        = pydicom.dcmread(dicom_file)
                        metadata.remove_private_tags()
                        metadata.save_as(dicom_file)

            line = input_file.readline()         
