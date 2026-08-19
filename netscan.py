#!/usr/bin/env python3

import json
import os
import platform
import time
import ipaddress
import socket
import urllib.request

import psutil

from scapy.all import ARP, Ether, srp


# CONFIGURATION

DEVICES_FILE = "devices.json"
OUI_FILE = "oui.csv"

OUI_URL = "https://standards-oui.ieee.org/oui/oui.csv"

# Update OUI database once every 24 hours
OUI_UPDATE_INTERVAL = 24 * 60 * 60


# SYSTEM

def get_system():
    system = platform.system()

    if system == "Linux":
        return "Linux"

    elif system == "Windows":
        return "Windows"

    elif system == "Darwin":
        return "macOS"

    elif system == "FreeBSD":
        return "FreeBSD"

    elif system == "OpenBSD":
        return "OpenBSD"

    elif system == "NetBSD":
        return "NetBSD"

    else:
        return system


# OUI DATABASE

def oui_database_needs_update():
    if not os.path.exists(OUI_FILE):
        return True

    try:
        last_update = os.path.getmtime(OUI_FILE)

        current_time = time.time()

        age = current_time - last_update

        return age >= OUI_UPDATE_INTERVAL

    except OSError:
        return True


def update_oui_database():

    if not oui_database_needs_update():

        print(
            "OUI database is up to date."
        )

        return

    print(
        "Updating OUI database..."
    )

    try:

        request = urllib.request.Request(
            OUI_URL,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 "
                    "(compatible; NetScan/1.0)"
                )
            }
        )

        with urllib.request.urlopen(
            request,
            timeout=15
        ) as response:

            data = response.read()

        with open(
            OUI_FILE,
            "wb"
        ) as file:

            file.write(data)

        print(
            "OUI database updated."
        )

    except Exception as e:

        if os.path.exists(OUI_FILE):

            print(
                "Could not update OUI database."
            )

            print(
                "Using cached OUI database."
            )

        else:

            print(
                "Could not download OUI database."
            )

            print(
                f"Error: {e}"
            )


def load_oui_database():

    oui_database = {}

    if not os.path.exists(OUI_FILE):
        return oui_database

    try:

        with open(
            OUI_FILE,
            "r",
            encoding="utf-8-sig"
        ) as file:

            for line in file:

                line = line.strip()

                if not line:
                    continue

                parts = line.split(",")

                if len(parts) < 3:
                    continue

                prefix = parts[1].strip()

                vendor = parts[2].strip().strip('"')

                prefix = (
                    prefix
                    .replace("-", "")
                    .replace(":", "")
                    .replace(".", "")
                    .upper()
                )

                if len(prefix) >= 6:

                    prefix = prefix[:6]

                    oui_database[prefix] = vendor

    except (
        OSError,
        UnicodeDecodeError
    ):

        return {}

    return oui_database


def get_vendor(
    mac,
    oui_database
):

    prefix = (
        mac
        .replace(":", "")
        .replace("-", "")
        .upper()[:6]
    )

    vendor = oui_database.get(
        prefix,
        "Unknown"
    )

    vendor = vendor.strip().strip('"')

    if vendor == "(Unknown)":
        vendor = "Unknown"

    return vendor


# NETWORK INFORMATION

def get_network_info(ip):

    interfaces = psutil.net_if_addrs()

    for interface, addresses in interfaces.items():

        for address in addresses:

            if address.family != socket.AF_INET:
                continue

            if address.address != ip:
                continue

            if not address.netmask:
                return interface, None

            try:

                network = ipaddress.ip_network(
                    f"{ip}/{address.netmask}",
                    strict=False
                )

                return (
                    interface,
                    str(network)
                )

            except ValueError:

                return interface, None

    return None, None


# ARP SCAN

def run_arp_scan(
    interface,
    network
):

    try:

        print(
            f"Scanning {network}..."
        )

        packet = (
            Ether(
                dst="ff:ff:ff:ff:ff:ff"
            )
            /
            ARP(
                pdst=network
            )
        )

        answered, _ = srp(
            packet,
            iface=interface,
            timeout=3,
            verbose=False
        )

        return answered

    except PermissionError:

        print()

        print(
            "Permission denied."
        )

        print(
            "Run the program with "
            "administrator/root privileges."
        )

        return None

    except Exception as e:

        print(
            f"Scan error: {e}"
        )

        return None


def parse_arp_output(
    answered,
    oui_database
):

    devices = []

    for _, received in answered:

        ip = received.psrc

        mac = received.hwsrc.lower()

        vendor = get_vendor(
            mac,
            oui_database
        )

        devices.append(
            {
                "ip": ip,
                "mac": mac,
                "vendor": vendor
            }
        )

    return devices


# JSON DATABASE

def load_devices():

    if not os.path.exists(
        DEVICES_FILE
    ):

        return {}

    try:

        with open(
            DEVICES_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(file)

    except (
        json.JSONDecodeError,
        OSError
    ):

        return {}


def save_devices(devices):

    try:

        with open(
            DEVICES_FILE,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                devices,
                file,
                indent=4,
                ensure_ascii=False
            )

    except OSError as e:

        print(
            f"Error saving devices: {e}"
        )


# DEVICE STATUS

def update_devices(
    found_devices,
    known_devices,
    network
):

    current_time = time.strftime(
        "%Y-%m-%d %H:%M:%S"
    )

    if network not in known_devices:

        known_devices[network] = {}

    network_devices = (
        known_devices[network]
    )

    for device in found_devices:

        mac = device["mac"]

        if mac not in network_devices:

            print(
                f"New device found: "
                f"{device['ip']} "
                f"{mac}"
            )

            network_devices[mac] = {

                "ip": device["ip"],

                "vendor": device["vendor"],

                "status": "ONLINE",

                "last_seen": current_time
            }

        else:

            network_devices[mac]["ip"] = (
                device["ip"]
            )

            network_devices[mac]["vendor"] = (
                device["vendor"]
            )

            network_devices[mac]["status"] = (
                "ONLINE"
            )

            network_devices[mac]["last_seen"] = (
                current_time
            )

    found_macs = {
        device["mac"]
        for device in found_devices
    }

    for mac in network_devices:

        if mac not in found_macs:

            network_devices[mac]["status"] = (
                "OFFLINE"
            )


# OUTPUT

def print_devices(
    devices,
    network
):

    network_devices = devices.get(
        network,
        {}
    )

    print()

    print("=" * 100)

    print(
        f"{'IP':<16}"
        f"{'MAC':<20}"
        f"{'Vendor':<50}"
        f"{'Status'}"
    )

    print("=" * 100)

    for mac, device in network_devices.items():

        print(
            f"{device['ip']:<16}"
            f"{mac:<20}"
            f"{device['vendor']:<50}"
            f"{device['status']}"
        )

    print("=" * 100)


# MAIN

def main():

    # Detect operating system

    system = get_system()

    print(
        f"Operating system: {system}"
    )

    print()

    # Update OUI database

    update_oui_database()

    print()

    oui_database = (
        load_oui_database()
    )

    print(
        f"OUI entries loaded: "
        f"{len(oui_database)}"
    )

    print()

    # Ask user for local IP

    ip = input(
        "Enter your local IP: "
    ).strip()

    print()

    # Find interface and network

    interface, network = (
        get_network_info(ip)
    )

    if interface is None:

        print(
            f"Interface for IP "
            f"{ip} not found."
        )

        return

    if network is None:

        print(
            "Could not determine "
            "network mask."
        )

        return

    print(
        f"Interface found: "
        f"{interface}"
    )

    print(
        f"Network: "
        f"{network}"
    )

    print()

    # Scan network

    answered = run_arp_scan(
        interface,
        network
    )

    if answered is None:
        return

    # Parse results

    found_devices = (
        parse_arp_output(
            answered,
            oui_database
        )
    )

    # Load database

    known_devices = (
        load_devices()
    )

    # Update device statuses

    update_devices(
        found_devices,
        known_devices,
        network
    )

    # Save database

    save_devices(
        known_devices
    )

    # Display results

    print_devices(
        known_devices,
        network
    )

    print()

    print(
        f"Devices found this scan: "
        f"{len(found_devices)}"
    )

    print(
        f"Known devices in this network: "
        f"{len(known_devices[network])}"
    )


# ENTRY POINT

if __name__ == "__main__":
    main()
