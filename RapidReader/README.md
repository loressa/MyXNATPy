Directory with tools for Rapid Reader integration in OHIF viewer plugin to XNAT.

Steps to follow to create the Visual Turing Test (VTT) in NCITA XNAT Cambridge, November 2021:

1 - Create the list of experiments to fill the Rapid Reader worklist(s).

This is done with the scriptlist_experiments.py. Edit information regarding xnathost, project_id_list, user_id and keyword. Then: python3 list_experiments.py. It will produce an output .csv file with the list of experiment.id in the given project, filtered with the given keyword.

2 - Create the randomised order of items for Rapid Reader worklist(s).

This is done using the make_random_lists.py script. Edit the user_id of the reader(s) for which the worklist(s) will be created, and give paths of input and output files, former containing the list of experiments filtered by e.g. omentum vs pelvic-ovarian disease in our example, and latter where the .txt file input to create the Rapid reader worklist will be stored. 


