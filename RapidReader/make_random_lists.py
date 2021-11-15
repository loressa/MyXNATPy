#!/usr/bin/env python

# Script written by Lorena Escudero (Department of Radiology, University of Cambridge)
# to make random lists of experiments, first with all omentum, then all pelvic cases

# Usage: edit input readers list and give paths for input and output files, then python3 make_random_lists.py

import sys

import numpy as np
import pandas as pd

input_readers = ['READERID']

input_file_omentum = 'INPUT_FILE_OMENTUM'
input_file_pelvic = 'INPUT_FILES_PELVIC'

df_omentum = pd.read_csv(input_file_omentum)
df_pelvic = pd.read_csv(input_file_pelvic)

for reader in input_readers:
    random_omentum = df_omentum.sample(frac=1).reset_index(drop=True)
    random_pelvic = df_pelvic.sample(frac=1).reset_index(drop=True)

    output_file = 'OUTPUT_PATH' + reader + '.txt'
    with open(output_file, 'w') as output:
        sys.stdout = output
        for i in range(len(random_omentum)):
            print(random_omentum['Experiment'][i])
        for i in range(len(random_pelvic)):
            print(random_pelvic['Experiment'][i])

