# Network Diagnostic Toolkit

## Project Overview
Network Diagnostic Toolkit is a Python-based command-line application designed to diagnose common network connectivity problems on Linux systems. It also supports Windows.

The toolkit helps users inspect network configuration, check internet connectivity, resolve domain names, analyze network routes, and test TCP ports.

## Features
- Display IP and network interface configuration.
- Detect the default network gateway.
- Check internet connectivity using ping.
- Perform DNS resolution.
- Automatically detect common network problems.
- Test college server connectivity.
- Analyze network routes using traceroute.
- Test TCP port connectivity.
- Generate diagnostic reports.

## Technologies Used
- Python 3
- Linux / Kali Linux
- Windows
- Socket programming
- Subprocess module
- Linux networking commands

## Project Structure
```text
network-diagnostic-toolkit/
│
├── main.py
├── diagnostics.py
├── requirements.txt
├── README.md
└── reports/
```

## Requirements
- Python 3
- Kali Linux or another Linux distribution
- Windows (optional)

Linux networking utilities:
```bash
sudo apt update
sudo apt install iproute2 iputils-ping traceroute -y
```

## Installation and Execution

### Linux / Kali Linux
1. Open the terminal.
2. Navigate to the project directory:
```bash
cd /mnt/d/Projects/network-diagnostic-toolkit
```
3. Run the application:
```bash
python3 main.py
```

### Windows
Open the project folder in the terminal and execute:
```bash
python main.py
```

## Diagnostic Modules

| Module | Purpose |
|---|---|
| IP Configuration | Displays network interface details |
| Default Gateway | Identifies the default gateway |
| Internet Connectivity | Checks internet access |
| DNS Resolution | Resolves domain names |
| Automatic Diagnosis | Detects common network problems |
| College Server Test | Checks server reachability |
| Network Route | Examines the route to a destination |
| TCP Port Test | Checks TCP port availability |
| Report Generation | Saves diagnostic results |

## Testing Results

The application was tested in Kali Linux running under WSL 2.

| Test | Result |
|---|---|
| IP Configuration | Successful |
| Default Gateway | Detected |
| Internet Connectivity | Connected |
| DNS Resolution | Successful |
| Automatic Diagnosis | Healthy |
| Network Route | Partially traced |
| TCP Port 443 | Open |

**Final Test Summary:**
- Tests performed: 7
- Successful tests: 6
- Failed tests: 0
- Inconclusive tests: 1

## Limitations
- Some routers may block traceroute probes.
- Some servers may block ICMP ping requests.
- WSL 2 uses a virtual network interface, so its IP address may differ from the physical computer's Wi-Fi IP.
- College server testing requires the actual server address.

## Conclusion
The Network Diagnostic Toolkit successfully performs basic network diagnostics and helps identify common connectivity issues. It provides a simple command-line interface for checking network configuration, internet access, DNS resolution, routing information, and TCP port connectivity.