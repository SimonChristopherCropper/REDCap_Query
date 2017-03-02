#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
-----------------------     REDCap_Query()    --------------------------

This script is used to extract a single field or group of fields from the same
event for every participant in a study.

The field constraint originates from the savelist() function where only records
that contain the secondary key (first field in 'specialfields' list) are kept
(see Constraint_#1). Although the data within other event-feild combos would
be downloaded they are not retained.

Programmed by Simon Christopher Cropper 19 October 2016
(c) Murdoch Childrens Research Institute

"""

#***********************************************************************
#***********************     GPLv3 License      ************************
#***********************************************************************
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#***********************************************************************

# import modules required to have python do what is required
import os                   # access to general operating system stuff
import platform             # access to platform details
import argparse
import csv                  # access to CSV library
import urllib.parse
import urllib.request

def extract_data_redcap(url, edrlist):

    """
    This function allows you to poll the REDCap API. The examples
    provided on the API Playground don't work in Python 3.
    """

    data = urllib.parse.urlencode(edrlist)
    data = data.encode('ascii') # data should be bytes
    req = urllib.request.Request(url, data)
    with urllib.request.urlopen(req) as response:
        response_buffer = response.read()

    response_text = response_buffer.decode("UTF-8")
    required_text = response_text.split('\n')
    return required_text

def savelist(targetlist, pythonscriptdir, outputfile, start):

    """
    This function saves the list to a file for use in
    programs like Excel.
    """

    csv_out = open(pythonscriptdir + outputfile, 'w', newline='',
                   encoding='UTF-8')

    mywriter = csv.writer(csv_out)

    if start.strip() == "IncludeHeader":
        startnum = 0
    else:
        startnum = 1

    counter = 0

    for row in targetlist:

        if counter >= startnum:

            if row != "":
                subrow = row.split(",")
                del subrow[1]
                # Constraint_#1: Filter out rows that do not have secondary key
                if subrow[1] != "":
                    for n in range(0,len(subrow)-1):
                        if type(subrow[n]) == str:
                            subrow[n] = subrow[n].replace('"','').strip()
                    mywriter.writerow(subrow)

        counter = counter + 1


    csv_out.close()

def main():

    """
    This is the main routine that call all the relevant modues in sequence.
    """

    parser = argparse.ArgumentParser()
    parser.add_argument("redcap_server", help="Enter the URL for the REDCap \
                        Server API, e.g. https://redcap.vanderbilt.edu/api")
    parser.add_argument("user_token", help="Enter the USER token provided by \
                        your REDCap Administrator, \
                        e.g. A945062DEAB165F74FC5C5E0BA14A265")
    parser.add_argument("primarykey", help="Enter the primary key for the \
                        person. e.g. RecordID")
    parser.add_argument("specialfields", help="Enter a list of fields to \
                        extract from an event. Only records with data in the \
                        first field will be kept, \
                        e.g. DOB,firstname,lastname")
    parser.add_argument("includeheader", help="if 'Header' will include \
                        list of field names on first line")
    parser.add_argument("output_file", help="name of file to save in \
                        the output directory")
    args = parser.parse_args()

    targetfield = args.specialfields.split(sep=",")[0]
    print("Extracting [" + targetfield + "] data from REDCap")

    # What platform are we on?
    if platform.system() == 'Windows':
        dirsymbol = '\\'
    else:
        dirsymbol = '/'

    pythonscriptdir = os.path.dirname(os.path.realpath(__file__))
    output_dir = "output_data"

    savepath = pythonscriptdir + dirsymbol + output_dir + dirsymbol
    savefile = args.output_file

    url = args.redcap_server

    primarykey = args.primarykey
    coreidenifiers = primarykey + ",redcap_event_name,"
    specialfields = args.specialfields

    data = {
        'token': args.user_token,
        'content': 'record',
        'format': 'csv',
        'type': 'flat',
        'fields':  coreidenifiers + specialfields,
        'rawOrLabel': 'raw',
        'rawOrLabelHeaders': 'raw',
        'exportCheckboxLabel': 'false',
        'exportSurveyFields': 'false',
        'exportDataAccessGroups': 'false',
        'returnFormat': 'csv',
    }

    mydata = extract_data_redcap(url, data)

    savelist(mydata, savepath, savefile, args.includeheader)

    print("CSV list saved to " + savepath + savefile)

if __name__ == "__main__":

    main()

