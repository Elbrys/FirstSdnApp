# FirstSdnApp

Two sample SDN applications that work with Elbrys' SDN Developer Lab (SDN platform-as-a-service).  See http://dev.elbrys.com.

One application, FirstSdnApp, uses Elbrys' OpenNAC api. A high-level api for controlling policy for endpoints connecting to your network.

The other application, FirstRestconfApp, uses the RESTCONF api of OpenDaylight to get the network topology.

Another application, FirstSdnAppSwitch, should be run on a Mininet VM.  It will create a Mininet switch and connect it to your instance of SDN Developer Lab.  Run this before running FirstSdnApp or FirstRestconfApp.

To get started quickly, check out https://github.com/Elbrys/SDN-Developer-Lab/wiki


# Current Version
1.0.1

# Prerequisites
   - A free account on Elbrys SDN Developer Lab 
       - Follow our [Quickstart](https://github.com/Elbrys/SDN-Developer-Lab/wiki)
   - An OpenFlow switch connected to it (virtual (Mininet) switch will work)
       - Follow our [Quickstart](https://github.com/Elbrys/SDN-Developer-Lab/wiki)
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
  --id ID          your SDN Developer Lab Application id. Go to sdn-developer. elbrys.com,
                   logon, select "My Account" in top right.
  --secret SECRET  your SDN Developer Lab Application secret. Go to sdn-
                   developer.elbrys.com, logon, select "My Account", select
                   "Edit Account", select the "eyeball" icon next to password.
  --server SERVER  The IP address of your SDN Developer Lab controller. Go to sdn-
                   developer.elbrys.com, logon, look at "Controller" table.
  --port PORT      The TCP REST API port number of your SDN Developer Lab controller. Go to
                   sdn-developer.elbrys.com, logon, look at "Controller" table
                   for REST API Port.
  --switch SWITCH  the Datapath Id (DPID) for the switch connected in SDN Developer Lab 
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
  --id ID          your SDN Developer Lab Application id. Go to sdn-developer. elbrys.com,
                   logon, select "My Account" in top right.
  --secret SECRET  your SDN Developer Lab Application secret. Go to sdn-
                   developer.elbrys.com, logon, select "My Account", select
                   "Edit Account", select the "eyeball" icon next to password.
  --server SERVER  The IP address of your SDN Developer Lab controller. Go to sdn-
                   developer.elbrys.com, logon, look at "Controller" table.
  --port PORT      The TCP REST API port number of your SDN Developer Lab controller. Go to
                   sdn-developer.elbrys.com, logon, look at "Controller" table
                   for REST API Port.
```

# FirstSwitch.py Usage

This must be run on a (virtual) machine running Mininet.  Obtain a pre-configured virtual machine image by going to your SDN Developer Lab page (https://sdn-developer.elbrys.com) and scrolling to the 'Devices' table and click the 'Download Mininet VM'.  Import that OVA file into your virtual machine manager.  
It will create a virtual switch with two hosts (endpoints).  It will connect the switch to your running instance of SDN Developer Lab. 
You can run FirstSwitch.py with -h flag to get its usage.

```bash
usage: FirstSwitch.py [-h] --id ID --server SERVER --port PORT

Simple Mininet application to create and connect Mininet switch to SDN Developer Lab.

optional arguments:
  -h, --help       show this help message and exit
  --id ID          your SDN Developer Lab Application id. Go to http://sdn-developer.elbrys.com,
                   logon, select "My Account" in top right.
  --server SERVER  The IP address of your SDN Developer Lab controller. Go to sdn-
                   developer.elbrys.com, logon, look at "Controller" table.
  --port PORT      The TCP OpenFlow API port number of your SDN Developer Lab controller. Go
                   to sdn-developer.elbrys.com, logon, look at "Controller"
                   table for OpenFlow Port.
```

# Example Command Line for FirstSdnApp
```
python FirstSdnApp.py --id Ra8beAb --secret H5tuNnQe --switch 5001871fc0  --server 1.2.3.4 --port 5678
```

# Other Example Applications - OpenNAC API
There is a Github repository for sample applications that use Elbrys' OpenNAC API.  If you clone this repository you will 
have a number of sample applications showing how to program SDN Developer Lab via the OpenNAC API.
   * https://github.com/Elbrys/ODL-S-Sample-Apps

# Other Example Applications - RESTCONF API
There is a Github repository for sample applications that use SDN Developer Lab controller's  RESTCONF API.  
These sample applications depend on a python library called pybvc.
   * Learn how to install the pybvc library here:  https://github.com/Brcdcomm/pybvc
   * Learn how to install the pybvcsampls (sample apps) here:  https://github.com/Brcdcomm/pybvcsamples


