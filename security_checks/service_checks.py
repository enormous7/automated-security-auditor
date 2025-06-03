# security_checks/service_checks.py

import subprocess
from config import UNNECESSARY_SERVICES

# ... (check_running_services 함수는 그대로 둡니다) ...

def check_open_ports():
    """
    Checks for unnecessarily open ports. (Uses 'ss' command, falls back to 'netstat' if 'ss' not found)
    """
    result = {"name": "Open Ports Check", "status": "PASS", "details": ""}
    open_ports = []

    # Try using 'ss' command first
    cmd_ss = "sudo ss -tulnp"
    cmd_netstat = "sudo netstat -tulnp" # Fallback command

    chosen_cmd = ""

    try:
        # Check if 'ss' command exists
        subprocess.run(["ss", "-h"], check=True, capture_output=True) # Check if 'ss' command is available
        chosen_cmd = cmd_ss
    except FileNotFoundError:
        # If 'ss' not found, try 'netstat'
        try:
            subprocess.run(["netstat", "-h"], check=True, capture_output=True) # Check if 'netstat' command is available
            chosen_cmd = cmd_netstat
        except FileNotFoundError:
            result["details"] = "Neither 'ss' nor 'netstat' command found. Please install one of them."
            result["status"] = "ERROR"
            return result

    try:
        output = subprocess.check_output(chosen_cmd, shell=True, text=True).strip()

        # Skip header line (depends on command, ss usually has 1 header line)
        # For 'ss', skip the first line; for 'netstat', skip first two.
        start_line = 1 if "ss " in chosen_cmd else 2

        for line in output.split('\n')[start_line:]:
            if "LISTEN" in line:
                parts = line.split()
                # For 'ss': Recv-Q Send-Q Local Address:Port Peer Address:Port Process
                # For 'netstat': Proto Recv-Q Send-Q Local Address Foreign Address State PID/Program name

                local_address_port_index = 3 if "ss " in chosen_cmd else 3 # Index of 'Local Address'
                process_info_index = -1 # Index of 'Process' or 'PID/Program name'

                if len(parts) > local_address_port_index:
                    local_address = parts[local_address_port_index]
                    if ':' in local_address:
                        port = local_address.split(':')[-1]

                        process_info = "N/A"
                        if len(parts) > process_info_index and parts[process_info_index]:
                            process_info = parts[process_info_index]

                        open_ports.append(f"Port {port} (Process: {process_info.split('/')[0].strip()})") # Extract process name only

        if open_ports:
            result["status"] = "WARN"
            result["details"] = f"The following ports are open: {'; '.join(open_ports)}. Unnecessary ports should be closed."
        else:
            result["details"] = "No open ports found."

    except subprocess.CalledProcessError as e:
        # Better error handling: check if stderr is not None before stripping
        error_details = e.stderr.strip() if e.stderr else "Unknown error from command execution."
        result["details"] = f"Command '{chosen_cmd}' execution failed: {error_details}. Please ensure you have sufficient permissions and the command is in your PATH."
        result["status"] = "ERROR"
    except FileNotFoundError:
        result["details"] = f"Command '{chosen_cmd.split()[1]}' not found. Please ensure it is installed and in your PATH."
        result["status"] = "ERROR"
    except Exception as e:
        result["details"] = f"An unexpected error occurred during port checking: {e}"
        result["status"] = "ERROR"
    return result