# NetScan

A Python-based local network scanner that discovers devices using ARP.

## Features

- ARP network scanning
- Automatic network detection from a local IP address
- MAC address detection
- Vendor detection using the IEEE OUI database
- Online/offline device tracking
- Separate device database for each network
- Automatic OUI database updates
- Operating system detection of the computer running NetScan
- JSON-based device database

## Requirements

- Python 3.10+
- Scapy
- psutil
- Administrator/root privileges for ARP scanning

## Installation

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/NetScan.git
cd NetScan


Install dependencies:

python3 -m pip install -r requirements.txt


Usage

Run NetScan with administrator/root privileges:

Linux / macOS:
sudo python3 netscan.py

Windows:
Run the terminal as Administrator:

python netscan.py


NetScan will ask for the local IP address:
Enter your local IP: 123.456.7.890

It will then determine the corresponding network interface and network:
Interface found: xxxxxx
Network: 123.456.7.8/00

The scanner will perform an ARP scan and display discovered devices.

EXAMPLE:
IP              MAC                 Vendor                                                                          Status
=======================================================================================================================================
123.456.7.8     60:a4:b7:bb:1e:7d  TP-Link Systems Inc                                                             ONLINE
123.456.7.89    44:a6:42:d1:94:ca  Hangzhou Hikvision Digital Technology Co.                                       ONLINE
123.456.7.890   3a:b7:82:75:b3:01  Unknown                                                                         ONLINE
123.456.7.891   88:b9:45:7b:f2:c2  Apple, Inc.                                                                     OFFLINE
=======================================================================================================================================


OUI Database

NetScan uses the IEEE OUI database to identify device manufacturers.
The database is automatically updated once every 24 hours.
If the update fails, NetScan uses the previously downloaded database.
The OUI database is stored locally as oui.csv and is excluded from Git using .gitignore.


Device Database

Discovered devices are stored in:
devices.json


Devices are grouped by network, allowing NetScan to remember devices from different networks.
The database stores:
-IP address
-MAC address
-Vendor
-Online/offline status
-Last seen time

devices.json is excluded from Git because it contains information about local network devices.


Project Structure:
NetScan/
├── netscan.py
├── requirements.txt
├── README.md
├── .gitignore
├── devices.json      # generated locally
└── oui.csv           # generated locally


License

MIT License
EOF
