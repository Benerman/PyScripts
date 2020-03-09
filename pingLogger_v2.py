#!/usr/bin/python3

"""
Pinger and logger to check for time of power issues
Debug output to console but adding additional arg

$ python3 pingLogger.py debug

intended use
$ nohup python3 pingLogger.py &
"""

import os, time, datetime, subprocess, logging, sys

if len(sys.argv) > 1:
        debug = True
        logging.basicConfig(level=logging.DEBUG)
else:
        debug = False



def log_it(data):
        with open("pingLogger.txt", 'a') as file:
                file.write('[{}]: {}\n'.format(datetime.datetime.now(), data))
                if debug:
                        logging.debug('[{}]: {}'.format(datetime.datetime.now(), data))


def pinger():
        google = subprocess.check_output('ping -c 4 google.com', shell=True)
        nas = subprocess.check_output('ping -c 4 10.251.146.237', shell=True)
        chimera = subprocess.check_output('ping -c 4 10.251.146.137', shell=True)
        hydra = subprocess.check_output('ping -c 4 10.251.147.188', shell=True)
        tpog_cc = subprocess.check_output('ping -c 4 10.251.146.17', shell=True)
        deadline = subprocess.check_output('ping -c 4 35.192.216.217', shell=True)
        google_dns = subprocess.check_output('ping -c 4 8.8.8.8', shell=True)
        return bool(google), bool(nas), bool(chimera), bool(hydra), bool(tpog_cc), bool(deadline), bool(google_dns)


def main():
        while True:
                log_it(pinger())
                time.sleep(600)
                pass

if __name__ == "__main__":
        main()
