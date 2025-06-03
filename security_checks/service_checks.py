# security_checks/service_checks.py

import subprocess
from config import UNNECESSARY_SERVICES

def check_running_services():
    """
    Checks for unnecessarily running services.
    """
    result = {"name": "Unnecessary Service Check", "status": "PASS", "details": ""}
    found_unnecessary_services = []
    try:
        # Get list of running services using systemctl list-units --type=service --state=running
        cmd = "systemctl list-units --type=service --state=running --no-pager"
        output = subprocess.check_output(cmd, shell=True, text=True).strip()
        
        running_services = []
        for line in output.split('\n'):
            parts = line.split()
            if len(parts) > 0 and parts[0].endswith(".service"):
                service_name = parts[0].replace(".service", "")
                running_services.append(service_name)
        
        for service in UNNECESSARY_SERVICES:
            if service in running_services:
                found_unnecessary_services.append(service)
        
        if found_unnecessary_services:
            result["status"] = "FAIL"
            result["details"] = f"The following unnecessary services are running: {', '.join(found_unnecessary_services)}"
        else:
            result["details"] = "No unnecessarily running services found."

    except subprocess.CalledProcessError as e:
        result["details"] = f"Command execution failed: {e.stderr.strip()}"
    except FileNotFoundError:
        result["details"] = "systemctl command not found."
    return result

def check_open_ports():
    """
    Checks for unnecessarily open ports. (Uses Netstat or ss command)
    """
    result = {"name": "Open Ports Check", "status": "PASS", "details": ""}
    open_ports = []
    try:
        # -t: TCP, -u: UDP, -l: Listening, -n: Numeric, -p: Process info
        cmd = "sudo netstat -tulnp" # May require sudo privileges
        output = subprocess.check_output(cmd, shell=True, text=True).strip()
        
        # Skip header lines and parse each line
        for line in output.split('\n')[2:]: # First two lines are headers
            if "LISTEN" in line:
                parts = line.split()
                # Extract port from local address (IP:Port)
                local_address = parts[3]
                if ':' in local_address:
                    port = local_address.split(':')[-1]
                    # Process information related to the port (if any)
                    process_info = parts[-1] if len(parts) > 5 else "N/A"
                    open_ports.append(f"Port {port} (Process: {process_info})")

        if open_ports:
            result["status"] = "WARN" # Set as warning, not all open ports are issues
            result["details"] = f"The following ports are open: {'; '.join(open_ports)}. Unnecessary ports should be closed."
        else:
            result["details"] = "No open ports found."

    except subprocess.CalledProcessError as e:
        result["details"] = f"Command execution failed: {e.stderr.strip()}. If 'sudo' is required, run with 'sudo python main.py'."
        result["status"] = "ERROR"
    except FileNotFoundError:
        result["details"] = "netstat or ss command not found."
        result["status"] = "ERROR"
    return result

# Add other necessary service-related check functions here.