# FirstSdnApp
Two sample SDN applications that work with Elbrys' OpenDaylight as a service (ODL-S).  See http://dev.elbrys.com.

One application, FirstSdnApp, uses Elbrys' OpenNAC api. A high-level api for controlling policy for endpoints connecting to your network.

The other application, FirstRestconfApp, uses the RESTCONF api of ODL-S to get the network topology.

Another application, FirstSdnAppSwitch, should be run on a Mininet VM.  It will create a Mininet switch and connect it to your ODL-S instance.  Run this before running FirstSdnApp or FirstRestconfApp.


# Current Version
1.0.1

# Prerequisites
   - A free account on Elbrys ODL-S 
       - Go to http://sdn-developer.elbrys.com and sign-up (or logon with your github account)
   - An OpenFlow switch connected to it (virtual (Mininet) switch will work)
       - Go to https://github.com/Elbrys/ODL-S/wiki/Connect-Network-Device and follow the instructions there
       - You can use instructions for Mininet and then use the FirstSdnAppSwitch.py found in this repository to create the switch for you.
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

# FirstSdnApp.py Usage

You can run FirstSdnApp.py with -h flag to get its usage.

```bash
usage: FirstSdnApp.py [-h] --id ID --secret SECRET --server SERVER --port PORT
                      --switch SWITCH

Simple SDN Application to block/unblock devices connected to switch.

optional arguments:
  -h, --help       show this help message and exit
  --id ID          your ODL-S Application id. Go to sdn-developer. elbrys.com,
                   logon, select "My Account" in top right.
  --secret SECRET  your ODL-S Application secret. Go to sdn-
                   developer.elbrys.com, logon, select "My Account", select
                   "Edit Account", select the "eyeball" icon next to password.
  --server SERVER  The IP address of your ODL-S server. Go to sdn-
                   developer.elbrys.com, logon, look at "Controller" table.
  --port PORT      The TCP REST API port number of your ODL-S server. Go to
                   sdn-developer.elbrys.com, logon, look at "Controller" table
                   for REST API Port.
  --switch SWITCH  the Datapath Id (DPID) for the switch connected in ODL-S
                   dashboard without ":" e.g. ccfa00b07b95 Go to sdn-
                   developer.elbrys.com, logon, look in "Devices" table
```

# FirstRestconfApp.py Usage

You can run FirstRestconfApp.py with -h flag to get its usage.

```bash
usage: FirstRestconfApp.py [-h] --id ID --secret SECRET --server SERVER --port
                           PORT

Simple SDN Application to block/unblock devices connected to switch.

optional arguments:
  -h, --help       show this help message and exit
  --id ID          your ODL-S Application id. Go to sdn-developer. elbrys.com,
                   logon, select "My Account" in top right.
  --secret SECRET  your ODL-S Application secret. Go to sdn-
                   developer.elbrys.com, logon, select "My Account", select
                   "Edit Account", select the "eyeball" icon next to password.
  --server SERVER  The IP address of your ODL-S server. Go to sdn-
                   developer.elbrys.com, logon, look at "Controller" table.
  --port PORT      The TCP REST API port number of your ODL-S server. Go to
                   sdn-developer.elbrys.com, logon, look at "Controller" table
                   for REST API Port.
```

# FirstSdnAppSwitch.py Usage

You can run FirstSdnAppSwitch.py with -h flag to get its usage.

```bash
usage: FirstSdnAppSwitch.py [-h] --id ID --server SERVER --port PORT

Simple Mininet application to create and connect Mininet switch to ODL-S.

optional arguments:
  -h, --help       show this help message and exit
  --id ID          your ODL-S Application id. Go to sdn-developer. elbrys.com,
                   logon, select "My Account" in top right.
  --server SERVER  The IP address of your ODL-S server. Go to sdn-
                   developer.elbrys.com, logon, look at "Controller" table.
  --port PORT      The TCP OpenFlow API port number of your ODL-S server. Go
                   to sdn-developer.elbrys.com, logon, look at "Controller"
                   table for OpenFlow Port.
```

# Example Command Line
```
python FirstSdnApp.py --id Ra8beAb --secret H5tuNnQe --switch 5001871fc0  --server 1.2.3.4 --port 5678
```

# Other Example Applications
There is a Github repository for ODL-S sample applications.  If you clone this repository you will 
have a number of sample applications showing how to program ODL-S.
   * https://github.com/Elbrys/ODL-S-Sample-Apps


