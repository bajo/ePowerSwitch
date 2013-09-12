ePowerSwitch
============

module to control ePowerSwitch power strips from Leunig

ePowerSwitch.py
---------------

    class EpsSwitch:
        getData():
        showStatus():
        setStatus(number, status): 
        
    class EpsSocket:

Usage of ePS.py
---------------

Return information and current state of the ePowerSwitch  on host 192.168.1.10, port 80 with admin/password

    python ePS.py 192.168.1.10 80 admin password get
        
    bajo's ePS
    +---------------+------------------+--------+--------------+
    | socket number | connected device | status | power cycles |
    +---------------+------------------+--------+--------------+
    |       1       |     monitor      |   On   |      28      |
    |       2       |    subwoofer     |   On   |      43      |
    |       3       |   outlet_strip   |   On   |      23      |
    |       4       |      router      |   On   |      22      |
    +---------------+------------------+--------+--------------+

Set socket number 2 to 'On' on host 192.168.1.10, port 80 with admin/password

    python ePS.py 192.168.1.10 80 admin password set 2 On
Set socket number 4 to 'Off' on host 192.168.1.10, port 80 with admin/password

    python ePS.py 192.168.1.10 80 admin password set 4 Off


License
-------
GPL v2. See LICENSE file for details.
