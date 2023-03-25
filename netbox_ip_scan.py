# Import necessary libraries
import os
from netaddr import IPNetwork, IPAddress
from netbox import NetBox
from pythonping import ping
import urllib3
import concurrent.futures

# Disable warnings from urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# Network
IP_PREFIX = os.environ.get("IP_PREFIX")
DHCP_POOL = os.environ.get("DHCP_POOL")

# Configure Netbox settings
NETBOX_HOST = os.environ.get("NETBOX_HOST")
NETBOX_PORT = os.environ.get("NETBOX_PORT")

api_url = os.environ.get("api_url")
api_token = os.environ.get("api_token")
nb = NetBox(host=NETBOX_HOST, port=NETBOX_PORT,
            auth_token=api_token, use_ssl=True)

# Set network to check
n = IPNetwork(IP_PREFIX)

# Create set of IP addresses in DHCP pool
dhcp_pool_set = set(IPNetwork(DHCP_POOL))

# Check availability of IP addresses


def check_ip(ip):
    # Skip network address
    if ip == n.network:
        return

    # Reserve network address
    if ip == n.ip:
        nb.ipam.create_ip_address(
            address=str(ip),
            status="reserved",
            description="Network Address"
        )
        return

    # Reserve DHCP pool
    if ip in dhcp_pool_set:
        ip_address = nb.ipam.get_ip_addresses(address=str(ip))
        if len(ip_address) > 0:
            # Update status and description of existing IP address
            if ping(str(ip), count=1, timeout=2).success():
                nb.ipam.update_ip_by_id(
                    ip_id=ip_address[0]["id"],
                    status="active",
                    description="Active IP Address"
                )
                print(f"IP address {ip} is active")
            else:
                nb.ipam.update_ip_by_id(
                    ip_id=ip_address[0]["id"],
                    status="dhcp",
                    description="DHCP Pool"
                )
                print(f"IP address {ip} is DHCP Pool")
        else:
            # Create new IP address
            if ping(str(ip), count=1, timeout=2).success():
                nb.ipam.create_ip_address(
                    address=str(ip),
                    status="active",
                    description="Active IP Address"
                )
                print(f"IP address {ip} is active")
            else:
                nb.ipam.create_ip_address(
                    address=str(ip),
                    status="dhcp",
                    description="DHCP Pool"
                )
                print(f"IP address {ip} is DHCP Pool")
        return

    # Check if IP address already exists in NetBox
    ip_address = nb.ipam.get_ip_addresses(address=str(ip))
    if len(ip_address) > 0:
        # Update status and description of existing IP address
        if ping(str(ip), count=1, timeout=2).success():
            nb.ipam.update_ip_by_id(
                ip_id=ip_address[0]["id"],
                status="active",
                description="Active IP Address"
            )
            print(f"IP address {ip} is active")
        else:
            nb.ipam.update_ip_by_id(
                ip_id=ip_address[0]["id"],
                status="reserved",
                description="Inactive IP Address"
            )
            print(f"IP address {ip} is not active")
    else:
        # Create new IP address
        if ping(str(ip), count=1, timeout=2).success():
            nb.ipam.create_ip_address(
                address=str(ip),
                status="active",
                description="Active IP Address"
            )
            print(f"IP address {ip} is active")
        else:
            nb.ipam.create_ip_address(
                address=str(ip),
                status="reserved",
                description="Inactive IP Address"
            )
            print(f"IP address {ip} is not active")


# Use concurrent.futures to run check_ip function in multiple threads
with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
    results = [executor.submit(check_ip, ip) for ip in n]
