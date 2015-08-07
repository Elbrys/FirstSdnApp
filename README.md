# FirstSdnApp
A sample SDN application that works with Elbrys' OpenDaylight as a service (ODL-S).  See http://dev.elbrys.com.

# Current Version
1.0.0

# Prerequisites
   - A free account on Elbrys ODL-S 
       - Go to http://sdn-developer.elbrys.com and sign-up (or logon with your github account)
   - An OpenFlow switch connected to it (virtual (Mininet) switch will work)
       - Go to https://github.com/Elbrys/ODL-S/wiki/Connect-Network-Device and follow the instructions there
   - Python 2.7.x: 
       - Test if your system already has it

         ```bash
         python --version
         ```
          - If it is installed you should see a response like this (the last digit may be different):

          ```
          Python 2.7.5
          ```
          - If it is not installed, then download and install: https://www.python.org/downloads/
   - pip:  
       - Test if your system already has it:

         ```bash
         pip --version
         ```
         - If it is installed you should see a response similar to this (as long as it is not an error response):

         ```bash
         pip 6.0.8 from /Library/Python/2.7/site-packages/pip-6.0.8-py2.7.egg (python 2.7)
         ```
         - If it is not installed, then download and install:  https://pip.pypa.io/en/stable/installing.html#install-pip
   - Requests Python library
      - pip install requests

# Usage
```bash
usage: FirstSdnApp.py [-h] --id ID --secret SECRET --switch SWITCH
                      [--server SERVER] [--port PORT]

Simple SDN Application to block/unblock devices connected to switch.

optional arguments:
  -h, --help       show this help message and exit
  --id ID          your ODL-S Application id. Go to sdn-developer.elbrys.com,
                   logon, select "My Account" in top right.
  --secret SECRET  your ODL-S Application secret. Go to sdn-
                   developer.elbrys.com, logon, select "My Account", select
                   "Edit Account", select the "eyeball" icon next to password.
  --switch SWITCH  the Datapath Id (DPID) for the switch connected in ODL-S
                   dashboard without ":" e.g. ccfa00b07b95 Go to sdn-
                   developer.elbrys.com, logon, look in "Devices" table
  --server SERVER  The IP address of your ODL-S server. Go to sdn-
                   developer.elbrys.com, logon, look at "Controller" table.
  --port PORT      The TCP port number of your ODL-S server. Go to sdn-
                   developer.elbrys.com, logon, look at "Controller" table.
```

# Example Command Line
```
python FirstSdnApp.py --id Ra8beAb --secret H5tuNnQe --switch 5001871fc0  --server 1.2.3.4 --port 5678
```

# Other Example Applications
There is a Github repository for ODL-S sample applications.  If you clone this repository you will 
have a number of sample applications showing how to program ODL-S.
   * https://github.com/Elbrys/ODL-S-Sample-Apps


