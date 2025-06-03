# security_checks/file_permission_checks.py

import os
from config import EXCLUDE_DIRS

def check_sensitive_file_permissions(paths):
    """
    Checks permissions of sensitive files/directories.
    E.g., /etc/passwd, /etc/shadow, /etc/sudoers, /etc/ssh/sshd_config, etc.
    """
    results = []
    
    # List of sensitive files and their expected permissions (octal)
    sensitive_files = {
        "/etc/passwd": 0o644,  # -rw-r--r--
        "/etc/shadow": 0o640,  # -rw-r----- (readable only by root and shadow group)
        "/etc/sudoers": 0o440, # -r--r-----
        "/etc/ssh/sshd_config": 0o600, # -rw-------
    }

    for path, expected_perm in sensitive_files.items():
        result = {"name": f"File Permission Check: {path}", "status": "PASS", "details": ""}
        if os.path.exists(path):
            current_perm = os.stat(path).st_mode & 0o777 # Get current permissions
            if current_perm != expected_perm:
                result["status"] = "FAIL"
                result["details"] = (
                    f"Permissions of file '{path}' differ from expected. "
                    f"Current: {oct(current_perm)}, Expected: {oct(expected_perm)}"
                )
            else:
                result["details"] = f"Permissions of file '{path}' are correct: {oct(current_perm)}"
        else:
            result["status"] = "WARN"
            result["details"] = f"File '{path}' not found."
        results.append(result)
    
    return results

def traverse_and_check_permissions(base_path='/', min_perm=0o755):
    """
    Traverses and checks permissions for all files/directories under the specified path.
    Identifies files with overly permissive permissions (e.g., 777).
    """
    results = []
    
    for dirpath, dirnames, filenames in os.walk(base_path):
        # Handle excluded directories
        dirnames[:] = [d for d in dirnames if os.path.join(dirpath, d) not in EXCLUDE_DIRS]
        
        for name in dirnames + filenames:
            path = os.path.join(dirpath, name)
            if not os.path.exists(path):
                continue
            
            try:
                # If it's a symbolic link, do not check permissions of the original file
                if os.path.islink(path):
                    continue

                mode = os.stat(path).st_mode
                perm = mode & 0o777 # Extract only actual permissions (e.g., 755)

                # Check for World-writable (everyone can write) files/directories
                if (perm & 0o002) == 0o002: # If other users have write permissions
                    results.append({
                        "name": f"Excessive Permissions (World-Writable) Check: {path}",
                        "status": "FAIL",
                        "details": f"Permissions of '{path}' are overly permissive (world-writable): {oct(perm)}"
                    })
                # Check for SetUID/SetGID bits (potential for privilege escalation)
                elif (mode & 0o4000) or (mode & 0o2000): # SetUID or SetGID
                    results.append({
                        "name": f"SetUID/SetGID Bit Check: {path}",
                        "status": "WARN",
                        "details": f"SetUID/SetGID bit is set on '{path}': {oct(perm)}"
                    })
                # Add other general permission checks if needed
                
            except PermissionError:
                # Ignore files that cannot be accessed due to permissions
                pass
            except Exception as e:
                results.append({
                    "name": f"File Permission Check Error: {path}",
                    "status": "ERROR",
                    "details": f"Error occurred: {e}"
                })
    return results