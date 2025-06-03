# security_checks/os_checks.py

import subprocess
import re
from config import MIN_PASSWORD_LENGTH, SSH_CONFIG_PATH

def check_password_policy():
    """
    Checks the password policy (minimum length).
    Verifies PASS_MIN_LEN value in /etc/login.defs on Linux systems.
    """
    result = {"name": "Password Policy Check", "status": "FAIL", "details": ""}
    try:
        # Read PASS_MIN_LEN value from /etc/login.defs
        cmd = "grep '^PASS_MIN_LEN' /etc/login.defs"
        output = subprocess.check_output(cmd, shell=True, text=True).strip()
        
        match = re.search(r'PASS_MIN_LEN\s+(\d+)', output)
        if match:
            min_len = int(match.group(1))
            if min_len >= MIN_PASSWORD_LENGTH:
                result["status"] = "PASS"
                result["details"] = f"Password minimum length: {min_len} (Recommended: {MIN_PASSWORD_LENGTH} or more)"
            else:
                result["details"] = f"Password minimum length: {min_len} (Recommended: {MIN_PASSWORD_LENGTH} or more) - Weak"
        else:
            result["details"] = "PASS_MIN_LEN not found in /etc/login.defs."

    except subprocess.CalledProcessError as e:
        result["details"] = f"Command execution failed: {e.stderr.strip()}"
    except FileNotFoundError:
        result["details"] = "/etc/login.defs file not found."
    return result

def check_root_login_ssh():
    """
    Checks if direct root login via SSH is prohibited.
    """
    result = {"name": "SSH Root Login Prohibition", "status": "FAIL", "details": ""}
    try:
        cmd = f"grep -E '^PermitRootLogin' {SSH_CONFIG_PATH}"
        output = subprocess.check_output(cmd, shell=True, text=True).strip()
        
        # Check value after removing comments
        line = output.split('\n')[-1] # Last valid line (not a comment)
        if "#" in line: # Ignore commented lines
            result["details"] = f"PermitRootLogin setting in SSH config is commented out or unclear: {line}"
            return result
        
        if "PermitRootLogin no" in line or "PermitRootLogin prohibit-password" in line:
            result["status"] = "PASS"
            result["details"] = "Direct root login via SSH is prohibited."
        else:
            result["details"] = f"SSH root login allowed setting detected: {line}"
    except subprocess.CalledProcessError:
        result["details"] = f"PermitRootLogin setting not found in SSH config file ({SSH_CONFIG_PATH})."
    except FileNotFoundError:
        result["details"] = f"SSH config file ({SSH_CONFIG_PATH}) not found."
    return result

def check_empty_passwords():
    """
    Checks for user accounts with empty passwords.
    Verifies if the second field (password hash) in /etc/shadow is empty.
    """
    result = {"name": "Empty Password Account Check", "status": "PASS", "details": ""}
    empty_password_users = []
    try:
        # Requires read permissions for /etc/shadow (usually root only)
        with open("/etc/shadow", 'r') as f:
            for line in f:
                parts = line.strip().split(':')
                if len(parts) > 1 and not parts[1]: # If password hash field is empty
                    empty_password_users.append(parts[0])
        
        if empty_password_users:
            result["status"] = "FAIL"
            result["details"] = f"Accounts with empty passwords found: {', '.join(empty_password_users)}"
        else:
            result["details"] = "No accounts with empty passwords found."
    except PermissionError:
        result["details"] = "Permission denied to read `/etc/shadow`. Run with root privileges."
        result["status"] = "ERROR"
    except FileNotFoundError:
        result["details"] = "`/etc/shadow` file not found."
        result["status"] = "ERROR"
    return result

# Add other necessary OS-related check functions here.
# E.g., UFW/iptables firewall status, SELinux/AppArmor status, etc.