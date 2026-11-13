
import subprocess
import socket
import platform
import os
import shutil
import json
from datetime import datetime


# ==========================================
# SYSTEM INFORMATION
# ==========================================

OS = platform.system()


def run_command(command, timeout=15):
    """Execute system commands safely."""

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=timeout
        )

        return result.stdout.strip() or result.stderr.strip()

    except subprocess.TimeoutExpired:
        return "Error: Command timed out."

    except FileNotFoundError:
        return f"Error: Command not found: {command[0]}"

    except Exception as error:
        return f"Error: {error}"


def get_hostname():
    return socket.gethostname()


# ==========================================
# IP CONFIGURATION
# ==========================================

def get_ip_configuration():
    print("\n========== NETWORK CONFIGURATION ==========")

    print("Computer Name:", get_hostname())
    print("Operating System:", OS)

    if OS == "Windows":
        command = ["ipconfig", "/all"]
    else:
        command = ["ip", "addr", "show"]

    result = run_command(command)

    print("\nIP Configuration:")
    print(result)

    return result


# ==========================================
# DEFAULT GATEWAY
# ==========================================

def get_default_gateway():
    print("\n========== DEFAULT GATEWAY ==========")

    gateway = find_default_gateway()

    if gateway:
        result = f"Default Gateway: {gateway}"
    else:
        result = "Default Gateway: NOT FOUND"

    print(result)
    return result


def find_default_gateway():
    """Extract the default gateway address."""

    if OS == "Windows":
        result = run_command(["route", "print", "-4"])

        for line in result.splitlines():
            parts = line.split()

            if (
                len(parts) >= 4
                and parts[0] == "0.0.0.0"
                and parts[1] == "0.0.0.0"
            ):
                return parts[2]

    else:
        result = run_command(
            ["ip", "route", "show", "default"]
        )

        for line in result.splitlines():
            parts = line.split()

            if "via" in parts:
                return parts[parts.index("via") + 1]

    return None


# ==========================================
# PING CONNECTIVITY
# ==========================================

def ping_host(host, count=4, timeout=2):
    """Ping a host using OS-specific arguments."""

    if OS == "Windows":
        command = [
            "ping", "-n", str(count),
            "-w", str(timeout * 1000), host
        ]
    else:
        command = [
            "ping", "-c", str(count),
            "-W", str(timeout), host
        ]

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=count * timeout + 5
        )

        return result.returncode == 0, (
            result.stdout.strip() or result.stderr.strip()
        )

    except subprocess.TimeoutExpired:
        return False, "Ping command timed out."

    except FileNotFoundError:
        return False, "Ping command is not installed."

    except Exception as error:
        return False, str(error)


def check_internet_connection():
    print("\n========== INTERNET CONNECTIVITY TEST ==========")

    success, result = ping_host("1.1.1.1")

    status = "CONNECTED" if success else "NOT CONFIRMED"

    print("Internet Status:", status)
    print(result)

    return {
        "status": status,
        "details": result
    }


# ==========================================
# DNS RESOLUTION
# ==========================================

def check_dns_resolution():
    print("\n========== DNS RESOLUTION TEST ==========")

    domain = input(
        "Enter domain name (default: google.com): "
    ).strip()

    if not domain:
        domain = "google.com"

    try:
        addresses = socket.getaddrinfo(domain, None)

        ips = sorted(set(
            address[4][0] for address in addresses
        ))

        print("DNS Status: SUCCESS")
        print("Domain:", domain)
        print("Resolved IPs:", ", ".join(ips))

        return {
            "status": "SUCCESS",
            "domain": domain,
            "ips": ips
        }

    except socket.gaierror as error:
        print("DNS Status: FAILED")
        print("Reason:", error)

        return {
            "status": "FAILED",
            "domain": domain,
            "error": str(error)
        }


# ==========================================
# AUTOMATIC NETWORK DIAGNOSIS
# ==========================================

def detect_network_problems():
    print("\n========== AUTOMATIC NETWORK DIAGNOSIS ==========")

    problems = []

    # Gateway test
    gateway = find_default_gateway()

    if not gateway:
        print("Gateway: NOT FOUND")
        problems.append("Default gateway not found.")

    else:
        print("Gateway:", gateway)

        success, details = ping_host(gateway, count=2)

        if success:
            print("Gateway Status: REACHABLE")
        else:
            print("Gateway Status: PING NOT CONFIRMED")
            print("Note: Gateway may block ICMP requests.")

    # Public IP test
    success, details = ping_host("1.1.1.1")

    if success:
        print("Public IP Connectivity: SUCCESS")
    else:
        print("Public IP Connectivity: NOT CONFIRMED")
        problems.append(
            "Public IP ping failed; internet may be unavailable "
            "or ICMP may be blocked."
        )

    # DNS test
    try:
        ip = socket.gethostbyname("google.com")

        print("DNS Resolution: SUCCESS")
        print("Resolved IP:", ip)

    except socket.gaierror:
        print("DNS Resolution: FAILED")
        problems.append(
            "DNS resolution failed for google.com."
        )

    # Summary
    print("\n========== DIAGNOSTIC SUMMARY ==========")

    if not problems:
        print("No network problems detected by these tests.")
    else:
        for number, problem in enumerate(problems, 1):
            print(f"{number}. {problem}")

    return {
    "overall_status": "HEALTHY" if not problems else "ISSUES DETECTED",
    "problems_detected": len(problems),
    "problems": problems,
    "message": (
        "No network problems detected by the performed tests."
        if not problems
        else "Network problems were detected. Check the listed issues."
    )
}


# ==========================================
# COLLEGE SERVER CONNECTIVITY
# ==========================================

def check_college_server():
    print("\n========== COLLEGE SERVER CONNECTIVITY ==========")

    server = input(
        "Enter college server IP or hostname: "
    ).strip()

    if not server:
        print("Server address cannot be empty.")
        return {"status": "NOT TESTED"}

    try:
        socket.getaddrinfo(server, None)

    except socket.gaierror:
        print("Unable to resolve server address.")

        return {
            "server": server,
            "status": "DNS FAILED"
        }

    success, result = ping_host(server)

    status = "REACHABLE" if success else "NOT CONFIRMED"

    print("\nServer:", server)
    print("Status:", status)
    print("\nTest Details:")
    print(result)

    return {
        "server": server,
        "status": status,
        "details": result
    }


# ==========================================
# NETWORK ROUTE ANALYSIS
# ==========================================


def analyze_network_route():
    """Trace the network route and summarize responding hops."""

    print("\n========== NETWORK ROUTE ANALYSIS ==========")

    destination = input(
        "Enter destination (default: google.com): "
    ).strip()

    if not destination:
        destination = "google.com"

    if OS == "Windows":

        if not shutil.which("tracert"):
            result = "tracert command not found."
            print(result)
            return {"status": "ERROR", "details": result}

        command = [
            "tracert", "-d", "-h", "15",
            "-w", "1000", destination
        ]

    else:

        if shutil.which("traceroute"):
            command = [
                "traceroute", "-n", "-m", "15",
                "-w", "1", destination
            ]

        elif shutil.which("tracepath"):
            command = [
                "tracepath", "-m", "15", destination
            ]

        else:
            result = "Install traceroute or tracepath first."
            print(result)
            return {"status": "ERROR", "details": result}

    print(f"\nTracing route to {destination}...")
    print("Please wait...\n")

    result = run_command(command, timeout=60)

    print(result)

    # Analyze traceroute output
    lines = result.splitlines()

    responding_hops = 0
    timeout_hops = 0
    destination_reached = False

    try:
        destination_ips = {
            item[4][0]
            for item in socket.getaddrinfo(destination, None)
        }
    except socket.gaierror:
        destination_ips = set()

    for line in lines:

        parts = line.split()

        if not parts or not parts[0].isdigit():
            continue

        hop_number = int(parts[0])

        if "*" in parts:
            timeout_hops += 1

        else:
            responding_hops += 1

            # Check whether destination responded
            if any(
                item.strip("()") in destination_ips
                for item in parts[1:]
            ):
                destination_reached = True

    if destination_reached:
        status = "DESTINATION REACHED"

    elif responding_hops > 0:
        status = "PARTIAL ROUTE - DESTINATION NOT CONFIRMED"

    else:
        status = "DESTINATION NOT REACHED"

    summary = {
        "destination": destination,
        "status": status,
        "responding_hops": responding_hops,
        "timeout_hops": timeout_hops,
        "destination_reached": destination_reached,
        "details": result
    }

    print("\n========== ROUTE ANALYSIS SUMMARY ==========")
    print("Destination:", destination)
    print("Status:", status)
    print("Responding Hops:", responding_hops)
    print("Timeout Hops:", timeout_hops)
    print("Destination Reached:", destination_reached)

    return summary


# ==========================================
# TCP PORT CONNECTIVITY TEST
# ==========================================

def check_tcp_port():
    """Test TCP connectivity to a server port."""

    print("\n========== TCP PORT CONNECTIVITY TEST ==========")

    host = input(
        "Enter server IP or hostname: "
    ).strip()

    if not host:
        print("Server address cannot be empty.")

        return {
            "status": "NOT TESTED"
        }

    try:
        port = int(input("Enter port number (e.g. 443): "))

        if not 1 <= port <= 65535:
            print("Invalid port number.")

            return {
                "server": host,
                "status": "INVALID PORT"
            }

    except ValueError:
        print("Please enter a valid port number.")

        return {
            "server": host,
            "status": "INVALID PORT"
        }

    try:
        with socket.create_connection(
            (host, port), timeout=5
        ):
            status = "OPEN"

    except socket.timeout:
        status = "TIMEOUT"

    except ConnectionRefusedError:
        status = "CLOSED / CONNECTION REFUSED"

    except OSError as error:
        status = f"CONNECTION FAILED: {error}"

    print("\nServer:", host)
    print("Port:", port)
    print("TCP Status:", status)

    return {
        "server": host,
        "port": port,
        "status": status
    }


# ==========================================
# DIAGNOSTIC REPORT GENERATION
# ==========================================



def generate_diagnostic_report(results):
    print("\n========== GENERATING REPORT ==========")

    report_folder = "reports"
    os.makedirs(report_folder, exist_ok=True)

    filename = datetime.now().strftime(
        "Network_Report_%Y%m%d_%H%M%S.txt"
    )

    filepath = os.path.join(report_folder, filename)

    passed = 0
    failed = 0
    inconclusive = 0

    for test_name, output in results.items():

        status = None

        if test_name == "IP Configuration":
            status = "SUCCESS" if output and not str(output).startswith("Error:") else "FAILED"

        elif test_name == "Default Gateway":
            status = "SUCCESS" if "Default Gateway:" in str(output) and "NOT FOUND" not in str(output) else "FAILED"

        elif test_name == "Internet Connectivity":
            status = output.get("status") if isinstance(output, dict) else None

        elif test_name == "DNS Resolution":
            status = output.get("status") if isinstance(output, dict) else None

        elif test_name == "Automatic Diagnosis":
            status = output.get("overall_status") if isinstance(output, dict) else None

        elif test_name == "College Server":
            status = output.get("status") if isinstance(output, dict) else None

        elif test_name == "TCP Port Test":
            status = output.get("status") if isinstance(output, dict) else None

        elif test_name == "Network Route":
            status = output.get("status") if isinstance(output, dict) else None

        if status in [
            "SUCCESS", "CONNECTED", "REACHABLE",
            "OPEN", "HEALTHY", "DESTINATION REACHED"
        ]:
            passed += 1

        elif status in [
            "FAILED", "DNS FAILED", "ISSUES DETECTED",
            "CLOSED / CONNECTION REFUSED"
        ]:
            failed += 1

        else:
            inconclusive += 1

    total = len(results)

    if failed > 0:
        overall_status = "ISSUES DETECTED"
    elif passed > 0:
        overall_status = "CONNECTIVITY AVAILABLE"
    else:
        overall_status = "INCONCLUSIVE"

    with open(filepath, "w", encoding="utf-8") as file:

        file.write("=" * 55 + "\n")
        file.write("       NETWORK DIAGNOSTIC TOOLKIT REPORT\n")
        file.write("=" * 55 + "\n\n")

        file.write(f"Date and Time: {datetime.now()}\n")
        file.write(f"Computer Name: {get_hostname()}\n")
        file.write(f"Operating System: {OS}\n\n")

        file.write("-" * 55 + "\n")
        file.write("DIAGNOSTIC TEST RESULTS\n")
        file.write("-" * 55 + "\n")

        for test_name, output in results.items():

            file.write(f"\n\n{test_name}\n")
            file.write("-" * 40 + "\n")

            if isinstance(output, (dict, list)):
                file.write(json.dumps(output, indent=4))
            else:
                file.write(str(output))

            file.write("\n")

        file.write("\n")
        file.write("=" * 55 + "\n")
        file.write("          FINAL NETWORK HEALTH SUMMARY\n")
        file.write("=" * 55 + "\n\n")

        file.write(f"Tests Performed: {total}\n")
        file.write(f"Successful Tests: {passed}\n")
        file.write(f"Failed Tests: {failed}\n")
        file.write(f"Inconclusive Tests: {inconclusive}\n\n")
        file.write(f"Overall Status: {overall_status}\n")

        file.write("\n" + "=" * 55 + "\n")
        file.write("             END OF REPORT\n")
        file.write("=" * 55 + "\n")

    print("\nReport generated successfully!")
    print("Tests Performed:", total)
    print("Successful:", passed)
    print("Failed:", failed)
    print("Inconclusive:", inconclusive)
    print("Overall Status:", overall_status)
    print("Saved at:", filepath)

    return filepath
