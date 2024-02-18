#!/bin/bash

# Check for Python
if ! command -v python &> /dev/null; then
    echo "Python is not installed. Please install Python."
    exit 1
fi

# Check for pip
if ! command -v pip &> /dev/null; then
    echo "pip is not installed. Please install pip."
    exit 1
fi

#Check for pip version
pip_version=$(pip --version | cut -d' ' -f2 | cut -d' ' -f1)

if [ "$pip_version" -lt 20 ]; then 
    echo "Upgrading pip..."
    pip install --upgrade pip
fi

#Install dependencies 
echo "Installing dependencies..."
pip install pyzmq numpy Pillow tkinter

#Get the IP address as input parameter
read -p "Enter IP address: " ip_address

# Run Python script with the IP address as an argument
python $(command -v sdrGUI.py) $ip_address