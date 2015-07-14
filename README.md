# FirstSdnApp
A sample SDN application that works with Elbrys' OpenDaylight as a service (ODL-S).  See http://dev.elbrys.com.

# Current Version
1.0.0

# Prerequisites
   - A free account on Elbrys ODL-S 
       - Go to http://dev.elbrys.com and follow the instructions there
   - An OpenFlow switch connected to it (virtual (Mininet) switch will work)
       - Go to http://dev.elbrys.com and follow the instructions there
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

SDN Application to redirect devices connected to switch to a url.

optional arguments:
  -h, --help       show this help message and exit
  --id ID          your ODL-S Application id. Go to sdn-developer.elbrys.com,
                   logon and then in the header of the
                   applications table find your application id.
  --secret SECRET  your ODL-S Application secret. Go to sdn-
                   developer.elbrys.com, logon and then in the header of the
                   applications table select the "eyeball" icon next to password.
  --switch SWITCH  the Local MAC address for the switch connected in ODL-S
                   dashboard without ":" e.g. ccfa00b07b95 Go to sdn-
                   developer.elbrys.com, logon, look in "Devices" table
```

# Other Example Applications
There is a Github repository for ODL-S sample applications.  If you clone this repository you will 
have a number of sample applications showing how to program ODL-S.
   * https://github.com/Elbrys/ODL-S-Sample-Apps



# Example Execution
```bash
Jamess-MacBook-Air:FirstSdnApp jeb$ python FirstSdnApp.py --id myappid --secret myappsecret  --switch 1
ODL-S App1
Version: 1.0
A very simple 'hello world' application that uses ODL-S.

DESCRIPTION:
    This is an extremely simple Python application that demonstrates how to use Elbrys ODL as a service - ODL-S (dev.elbrys.com) to
    control endpoint user sessions access to the network.

    This application will connect to one of the switches that you have connected in the ODL-S portal (sdn-developer.elbrys.com)
    and demonstrate blocking and unblocking of network traffic for any device connected to the switch. 

PRE-REQUISITES:
   1.  Python 2.x
   2.  Install python-requests:
        a.  sudo easy_install requests
   3.  Go to dev.elbrys.com and follow the directions there


Mail bug reports and suggestion to : support@elbrys.com

Obtaining authorization token...
...authorization token obtained:eyJhbGciOiJIUzI1NiJ9.eyJleHAiOjE0MzQzMDc1OTYsInN1YiI6IjE3OTNiMmJmLTI3ZDEtNDhlZS1iYWQzLTY1NzczZDM0NTY1OCIsImlzcyI6IkFQRSIsInRnZW4iOjEsImlhdCI6MTQzNDIyMTE5Nn0.6GK7tHuFg_qJixyp216GITpcgK6ajCjaUMoIQ4JYm1s
Creating application...
...application created with id:1434165607930.  Now that an application is connected to your 
switch traffic of connected user devices will be blocked until a policy is defined.
Connect a user device (laptop, tablet, phone) to a port on your network device.
Press Enter when you have connected a user device.
From your user device prove to yourself you do NOT have connectivity.  Ping something.
Press Enter when you have proven your user device is blocked.
Creating authenticated policy as default for any device detected...
...authenticated policy created with id:1434165607931
From your user device prove to yourself you now DO have connectivity.  Try to ping something.
Press Enter when you have proven connectivity to yourself.
Deleting application...
...application deleted.  Once the application is deleted you will continue to have connectivity.
```

