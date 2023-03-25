# NetBox IP Scaner

This script allows you to scan a specified IP prefix for the required pool of IP addresses, some of which may be designated as DHCP pools. During the scanning process, the script checks the availability of each IP address and creates a record in NetBox depending on the status of the address.

## Prerequisites

Before using the script, you will need to specify the following variables:

```shell
IP_PREFIX = "192.168.2.0/23" #The IP prefix to scan.
DHCP_POOL = "192.168.3.240/28" #The DHCP pool of IP addresses.

NETBOX_HOST = "netbox.local" #The hostname or IP address of the NetBox server.
NETBOX_PORT = "443" #The port number to connect to the NetBox server.

api_url = "https://netbox.local/" #The API URL of the NetBox server.
api_token = "your_api_token" #The API token to authenticate with the NetBox server.
```

## How it works

The main purpose of this script is to automatically check a list of required IP addresses for availability and record them in NetBox. This allows you to keep track of available IP addresses and helps prevent IP address conflicts.

The script first scans the specified IP prefix and identifies the IP addresses that are part of the DHCP pool. It then checks the availability of each IP address using a simple ping command. If the IP address is available, the script creates a record in NetBox with the appropriate information, including the IP address, status, and DHCP status.

## Conclusion

The NetBox IP Scanner script allows you to automate the process of checking and recording available IP addresses in NetBox. This helps you keep track of your IP address space and prevents conflicts. By specifying the required variables and running the script, you can quickly and easily scan your IP prefix and update NetBox with the latest information.
