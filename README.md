[NetScan README — macOS support.md](https://github.com/user-attachments/files/31222677/NetScan.README.macOS.support.md)
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
- Windows, Linux and macOS support

---

# Requirements

## Windows

- Windows 10 or newer
- Python 3.10+
- Git
- Npcap
- Administrator privileges for network scanning

## Linux

- Python 3.10+
- Git
- `arp-scan`
- Scapy
- psutil
- Root privileges for ARP scanning

## macOS

- macOS 11 (Big Sur) or newer
- Python 3.10+
- Git
- Scapy
- `libpcap`
- Administrator privileges for network scanning

---

# Installation

## Windows

### 1. Install Python

Download Python from the official website:

[https://www.python.org/downloads/windows/](https://www.python.org/downloads/windows/)

During installation, enable:

```text
Add Python to PATH
```

Check the installation:

```text
python --version
```

Example:

```text
Python 3.14.6
```

### 2. Install Git

Download Git from:

[https://git-scm.com/download/win](https://git-scm.com/download/win)

Check the installation:

```text
git --version
```

### 3. Install Npcap

NetScan uses Scapy for packet operations. On Windows, Layer 2 packet operations require Npcap.

Download Npcap from:

[https://npcap.com/](https://npcap.com/)

Install it using the default settings.

If the installer shows:

```text
Install Npcap in WinPcap API-compatible Mode
```

enable this option.

After installation, restart PowerShell.

### 4. Clone NetScan

Open PowerShell and run:

```text
cd $HOME
git clone https://github.com/Chupeppek/NetScan.git
cd NetScan
```

### 5. Install dependencies

```text
python -m pip install -r requirements.txt
```

### 6. Run NetScan

Run PowerShell as Administrator and execute:

```text
python netscan.py
```

NetScan will detect your local network and scan it.

---

# macOS

## 1. Install Homebrew

NetScan requires `libpcap` for low-level network packet operations.

If Homebrew is not installed, install it from:

[https://brew.sh/](https://brew.sh/)

Check the installation:

```text
brew --version
```

## 2. Install system dependencies

Install `libpcap` and Git:

```text
brew install libpcap git
```

Check `libpcap`:

```text
tcpdump --version
```

macOS normally includes `tcpdump` and packet-capture support, but installing the Homebrew version of `libpcap` ensures the required library is available.

## 3. Install Python

If Python is not installed, install it with Homebrew:

```text
brew install python
```

Check the installation:

```text
python3 --version
```

Example:

```text
Python 3.14.6
```

## 4. Clone NetScan

Open Terminal and run:

```text
cd ~
git clone https://github.com/Chupeppek/NetScan.git
cd NetScan
```

## 5. Create a virtual environment

Create a Python virtual environment:

```text
python3 -m venv .venv
```

Activate it:

```text
source .venv/bin/activate
```

## 6. Install Python dependencies

Install the required Python packages:

```text
python3 -m pip install -r requirements.txt
```

## 7. Run NetScan

Run NetScan with administrator privileges:

```text
sudo .venv/bin/python netscan.py
```

macOS may ask for your user password.

NetScan will detect your local network and perform an ARP scan.

---

# Linux

## 1. Install system dependencies

### Debian / Ubuntu

```text
sudo apt update
sudo apt install python3 python3-pip python3-venv git arp-scan
```

### Fedora

```text
sudo dnf install python3 python3-pip python3-virtualenv git arp-scan
```

Check the installations:

```text
python3 --version
git --version
arp-scan --version
```

## 2. Clone NetScan

```text
git clone https://github.com/Chupeppek/NetScan.git
cd NetScan
```

## 3. Create a virtual environment

```text
python3 -m venv .venv
```

Activate it:

```text
source .venv/bin/activate
```

## 4. Install Python dependencies

```text
python3 -m pip install -r requirements.txt
```

## 5. Run NetScan

Run with root privileges:

```text
sudo .venv/bin/python netscan.py
```

If you are not using a virtual environment:

```text
sudo python3 netscan.py
```

---

# Usage

NetScan will ask for the local IP address:

```text
Enter your local IP: 123.456.7.890
```

It will then determine the corresponding network interface and network:

```text
Interface found: Ethernet
Network: 123.456.7.8/00
```

The scanner will perform an ARP scan and display discovered devices.

Example:

```text
IP              MAC                 Vendor                                                                          Status
=======================================================================================================================================
123.456.7.8      xx:xx:xx:xx:xx:xx  TP-Link Systems Inc                                                             ONLINE
123.456.7.89     xx:xx:xx:xx:xx:xx  Hangzhou Hikvision Digital Technology Co.                                       ONLINE
123.456.7.890    xx:xx:xx:xx:xx:xx  Unknown                                                                         ONLINE
123.456.7.891    xx:xx:xx:xx:xx:xx  Apple, Inc.                                                                     OFFLINE
=======================================================================================================================================
```

---

# OUI Database

NetScan uses the IEEE OUI database to identify device manufacturers.

The database is automatically updated once every 24 hours.

If the update fails, NetScan uses the previously downloaded database.

The OUI database is stored locally as:

```text
oui.csv
```

The file is excluded from Git using `.gitignore`.

---

# Device Database

Discovered devices are stored in:

```text
devices.json
```

Devices are grouped by network, allowing NetScan to remember devices from different networks.

The database stores:

- IP address
- MAC address
- Vendor
- Online/offline status
- Last seen time

`devices.json` is excluded from Git because it contains information about local network devices.

---

# Troubleshooting

## Windows: `winpcap is not installed`

If you see an error similar to:

```text
Scan error: Sniffing and sending packets is not available at layer 2:
winpcap is not installed.
```

Install Npcap:

[https://npcap.com/](https://npcap.com/)

During installation, enable:

```text
Install Npcap in WinPcap API-compatible Mode
```

Then restart PowerShell and run NetScan again.

## Windows: `No libpcap provider available`

You may see:

```text
WARNING: No libpcap provider available ! pcap won't be used
```

This warning alone does not necessarily prevent NetScan from working.

If the scan fails with a Layer 2 / WinPcap error, install Npcap as described above.

## macOS: permission denied

If NetScan cannot access the network interface or fails during ARP scanning, run it with administrator privileges:

```text
sudo .venv/bin/python netscan.py
```

macOS may also ask for permission for applications or terminals to access network-related resources.

## macOS: `libpcap` or packet capture errors

Make sure `libpcap` is installed:

```text
brew install libpcap
```

You can also check that packet capture is available:

```text
tcpdump --version
```

Then try running NetScan again with `sudo`.

## Linux: `arp-scan: command not found`

Install `arp-scan`.

Debian / Ubuntu:

```text
sudo apt install arp-scan
```

Fedora:

```text
sudo dnf install arp-scan
```

## Linux: permission denied

Run NetScan with root privileges:

```text
sudo .venv/bin/python netscan.py
```

---

# Updating NetScan

To download the latest version:

```text
cd NetScan
git pull
```

Update Python dependencies if necessary.

Windows:

```text
python -m pip install -r requirements.txt --upgrade
```

Linux:

```text
python3 -m pip install -r requirements.txt --upgrade
```

macOS:

```text
python3 -m pip install -r requirements.txt --upgrade
```

---

# Project Structure

```text
NetScan/
├── netscan.py
├── requirements.txt
├── README.md
├── .gitignore
├── devices.json      # generated locally
└── oui.csv           # generated locally
```

---

# Security and Privacy

NetScan is intended for scanning networks that you own or have permission to test.

Only scan networks where you have authorization.

The local device database may contain IP and MAC addresses from your network. Do not publish `devices.json` if you do not want to disclose information about your local network.

---

# License

MIT License
