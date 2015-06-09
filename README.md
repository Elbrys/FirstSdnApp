# FirstSdnApp
A sample SDN application that works with Elbrys' OpenDaylight as a service (ODL-S).

# Current Version
1.0.0

# Prerequisites
   - A free account on Elbrys ODL-S
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
usage: app1.py [-h] [--wait WAIT] --user USER --password PASSWORD --switch
               SWITCH

SDN Application to redirect devices connected to switch to a url.

optional arguments:
  -h, --help           show this help message and exit
  --wait WAIT          the number of seconds the application will pause to
                       allow you to connect end user device to switch to try
                       it out.
  --user USER          your ODL-S Account Username. Go to sdn-
                       developer.elbrys.com, logon, select "My Account" in top
                       right.
  --password PASSWORD  your ODL-S Account Password. Go to sdn-
                       developer.elbrys.com, logon, select "My Account",
                       select "Edit Account", select the "eyeball" icon next
                       to password.
  --switch SWITCH      the Local MAC address for the switch connected in ODL-S
                       dashboard without ":" e.g. ccfa00b07b95 Go to sdn-
                       developer.elbrys.com, logon, look in "Devices" table
```

# Example Execution
```bash
 python ./app1.py --user myusername --password mypassword --switch ccfa00b07b95 --wait 120

ODL-S App1
Version: 1.0

DESCRIPTION:
    This is an example Python application that demonstrates how to use Elbrys ODL as a service - ODL-S (dev.elbrys.com) to
    control endpoint user sessions access to the network.

    This application will connect to one of the switches that you have connected in the ODL-S portal (sdn-developer.elbrys.com)
    and redirect all endpoints that connect to the switch to a specific url.

PRE-REQUISITES:
   1.  Python 2.x
   2.  Install python-requests:
        a.  sudo easy_install requests
   3.  Go to dev.elbrys.com and follow the directions there


TRY IT OUT WHILE IT IS RUNNING: 
   1.  Connect a user device (laptop, phone, tablet, etc.) to your switch 
   2.  On the user device, if you are not redirected automatically, open your web browser, browse to a non https url (www.amazon.com).
       You will be redirected to www.elbrys.com.  You should be able to browse to www.elbrys.com
       (this is because the IP address of www.elbrys.com is whitelisted)
 
Mail bug reports and suggestion to : support@elbrys.com

Obtaining authorization token...
...authorization token obtained:eyJhbGciOiJIUzI1NiJ9.eyJleHAiOjE0MzM5NzU3ODEsInN1YiI6IjZmN2Y0NjZlLTZhNDItNGMxMy1iOGFjLTQzMzJlOTljOGZiNiIsImlzcyI6IkFQRSIsInRnZW4iOjEsImlhdCI6MTQzMzg4OTM4MX0.mvjrOCovnY5NMF0Lq9aGY8ZKNT6W_nFWNRru6SieUBI
Creating application...
...application created with id:1412228378082
Creating unauthenticated policy as default...
...unauthenticated policy created with id:1412228378083
Waiting 120 seconds for you to associate an endpoint and try default policy. Open browser try to go to a url...
...done waiting.
Deleting application...
...application deleted.
```

