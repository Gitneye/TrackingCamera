# Check for Python
if (!(Get-Command python -ErrorAction SilentlyContinue)) {
    Write-Host "Python is not installed. Please install Python."
    exit 1
}

# Check for pip
if (!(Get-Command pip -ErrorAction SilentlyContinue)) {
    Write-Host "pip is not installed. Please install pip."
    exit 1
}

# Check for pip version
$pip_version = pip --version | ForEach-Object { $_.Split(' ')[-1].Split('.')[0] }

if ($pip_version -lt 20) {
    Write-Host "Upgrading pip..."
    python -m pip install --upgrade pip
}

# Install dependencies
Write-Host "Installing dependencies..."
python -m pip install pyzmq numpy Pillow Tk

# Get IP address as input parameter
$ip_address = Read-Host "Enter IP address"

# Run Python script with the IP address as an argument
python sdrGUI.py $ip_address
