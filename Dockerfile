# Use Python 3.11 as the base image
FROM python:3.11

# Set working directory
WORKDIR /app

# Copy the requirements file
COPY requirements.txt .

# Upgrade pip
RUN pip install --upgrade pip

# Install required Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables
ENV IP_PREFIX="192.168.2.0/23"
ENV DHCP_POOL="192.168.3.240/28"
ENV NETBOX_HOST="netbox.local"
ENV NETBOX_PORT="443"
ENV API_URL="https://netbox.local/"
ENV API_TOKEN="your_api_token"

# Copy the script to the container
COPY netbox_ip_scan.py .

# Run the script when the container starts
CMD ["python3", "netbox_ip_scan.py"]
