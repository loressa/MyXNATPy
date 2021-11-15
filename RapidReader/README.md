Directory with tools for Rapid Reader integration in OHIF viewer plugin to XNAT.

Steps to follow to create the Visual Turing Test (VTT) in NCITA XNAT Cambridge, November 2021:

1 - Create the list of experiments to fill the Rapid Reader worklist(s).

This is done with the scriptlist_experiments.py. Edit information regarding xnathost, project_id_list, user_id and keyword. Then: python3 list_experiments.py. It will produce an output .csv file with the list of experiment.id in the given project, filtered with the given keyword.



