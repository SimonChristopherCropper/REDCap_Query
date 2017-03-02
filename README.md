# REDCap Query

The program is designed to extract fields from a REDCap instance and save them to CSV format (Participant_ID, Field_Value, Field_Value). For example it can be used to extract the **First Name**, **Last Name** and **Date of Birth** for all participants in a study.

Rather than calling the project directly, the REDCap API Server, and USER Token are fed into the routine using a batch/bash script so the code can be shared.

The batch/bash script needs to be created by the individual user using their user token. The script's one line includes...

    python [path]REDCap_Query.py REDCapServerAPI_URL USER_Token Fieldlist

>**[path]** = optional path to directory where routine is present

>**REDCapServerAPI_URL** = URL for the REDCap Server API, e.g. https://redcap.vanderbilt.edu/api

>**USER_Token** = USER token provided by your REDCap Administrator, e.g. A945062DEAB165F74FC5C5E0BA14A265

>**Fieldlist** = List of fieldnames separated by commas, e.g. firstname,lastname,dob

