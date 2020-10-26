Pipeline to clean a project and change the scan dates as difference with respect to admission dates.

1 - Run find_sessions.py to find the sessions of certain type (e.g. XRay, CT, etc) uploaded per patientID
a) python3 find_sessions.py AdmissionDate_batch0.csv > sessions_batch0.txt
b) check for not found subjects and remove those lines from .txt

2 - Run the anon cleaning of few DICOM tags. Afterwards check the .sh and remove lines with ATTN
a) sudo python3 clean_and_anon.py sessions_batch0.txt > batch0.sh
b) check for 'ATTN' lines in batch0.sh, check those with no ImageType at all, remove those lines
c) sudo sh batch0.sh

3 - Change date (and check if there is any strange tag changed!)
a) check/edit input_path in change_date.py
b) sudo python3 change_date.py AdmissionDate_batch0.csv > change_date_batch0.txt
c) check for lines with 'ATTN' and check if it makes sense to change those flagged tags

4 - Upload clean directories to new XNAT project
ls -d /path/to/clean/dirs/ > input_dirs_batch0.txt  
sudo python3 upload_dirs.py input_dirs_batch0.txt 
