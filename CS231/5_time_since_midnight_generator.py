"""
* Assigment 5
* Created by: Gregory Boyer
* Due: 9/27/20
* CS 231, Fall 2020
* Description: Demonstrate the use of a generator that indicates for each event in
access_log the number of seconds elapsed since the most recent midnight

args:
num_results (str): Optional argument for number of results returned
"""

import re
import argparse
from datetime import datetime



#define the file we'll be parsing
file_path = '/etc/httpd/logs/access_log'


def sec_from_midnight(file_path: str):
    """
    This function converts the string containing a datetime in the access logs to a datetime object
    and extracts the datetime and total number of seconds from the timestamp, representing number of seconds
    since midnight

    Param:
    file_path (str) --> The filepath representing the log

    Output:
    timestamp (str) --> printable string of datetime
    sec_elapsed (int) --> The number of seconds elapsed
    """

    for line in open(file_path):

        timestamp = re.search('(?<=\[).{20}', line).group(0)
        # ignore timezone, the assumption is that the calculation being done for this exercise is in the timezone of the log
        #convert string to datetime
        results_dt = datetime.strptime(timestamp, '%d/%b/%Y:%H:%M:%S')
        # do some math to calculate seconds
        sec_elapsed = results_dt.hour * 60 * 60 + results_dt.minute * 60 + results_dt.second

        yield timestamp, sec_elapsed


def main(args):
    num_results = args.num_results


    # This is written as a for loop so that larger chunks can be returned in the future.
    # error handling allows us to gracefully reach the end of the file
    gen = sec_from_midnight(file_path)

    for _ in range(num_results):
        try:
            # used a generator followed by a function in order to return both timestamp AND seconds, for comparison
            curr_timestamp, sec_elapsed = next(gen)

            print(curr_timestamp, 'elapsed seconds:', sec_elapsed)
        except StopIteration:
            pass


if __name__ == '__main__':
    # use argparse to create an optional argument for number of rows printed
    parser = argparse.ArgumentParser(
        description='Parses a file and returns datetime and seconds since midnight from log')
    parser.add_argument('num_results', type=int, default=10, nargs='?', help='Optional argument for number of results returned')
    args = parser.parse_args()

    # execute program
    main(args)
