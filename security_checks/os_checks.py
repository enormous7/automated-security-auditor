# security_checks/os_checks.py

import subprocess
import re
from config import MIN_PASSWORD_LENGTH, SSH_CONFIG_PATH

import subprocess
import re # 정규표현식 모듈 추가

def check_password_policy():
    result = {
        "check": "Password Policy Enforcement (PASS_MIN_LEN)",
        "status": "Fail", # 기본값은 Fail로 설정
        "details": ""
    }
    cmd = "grep '^PASS_MIN_LEN' /etc/login.defs"

    try:
        # stderr=subprocess.PIPE를 추가하여 에러 출력을 캡처
        output = subprocess.check_output(cmd, shell=True, text=True, stderr=subprocess.PIPE).strip()
        
        # grep이 성공적으로 패턴을 찾았을 때
        match = re.search(r'PASS_MIN_LEN\s+(\d+)', output)
        if match:
            min_len = int(match.group(1))
            if min_len >= 8: # 일반적인 최소 길이 기준 8을 가정
                result["status"] = "Pass"
                result["details"] = f"Password minimum length set to {min_len} characters."
            else:
                result["status"] = "Fail"
                result["details"] = f"Password minimum length is set to {min_len} characters, which is less than the recommended 8."
        else:
            # grep이 결과를 반환했지만, 정규식 매칭이 안 된 경우 (예: 주석 처리된 라인)
            result["status"] = "Fail"
            result["details"] = f"PASS_MIN_LEN setting not clearly found or improperly formatted in /etc/login.defs output: '{output}'"

    except subprocess.CalledProcessError as e:
        # grep이 패턴을 찾지 못하여 exit status 1을 반환한 경우
        if e.returncode == 1 and not e.stderr.strip(): # stderr가 비어있다면 패턴을 못 찾았을 가능성 높음
            result["status"] = "Fail"
            result["details"] = "Password minimum length (PASS_MIN_LEN) setting not found in /etc/login.defs or is commented out."
        else:
            # 다른 종류의 CalledProcessError 또는 stderr에 내용이 있는 경우
            error_output = e.stderr.strip() if e.stderr else "No stderr output available."
            result["status"] = "Fail"
            result["details"] = f"Command execution failed with exit code {e.returncode}: {error_output}"
    
    except Exception as e:
        # 기타 예상치 못한 오류
        result["status"] = "Error"
        result["details"] = f"An unexpected error occurred: {e}"

    return result

# 필요한 경우 다른 함수들도 유사하게 오류 처리 로직을 개선

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

# security_checks/os_checks.py

# ... (기존 코드) ...

def check_empty_passwords():
    """
    Checks for user accounts with empty passwords.
    Verifies if the second field (password hash) in /etc/shadow is empty.
    """
    result = {"name": "Empty Password Account Check", "status": "PASS", "details": ""}
    empty_password_users = []
    try:
        # /etc/shadow 파일 읽기 권한 필요 (보통 root만 가능)
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
        result["details"] = "Permission denied to read `/etc/shadow`. This check requires root privileges. Please run the script with 'sudo'."
        result["status"] = "ERROR"
    except FileNotFoundError:
        result["details"] = "`/etc/shadow` file not found."
        result["status"] = "ERROR"
    return result


# Add other necessary OS-related check functions here.
# E.g., UFW/iptables firewall status, SELinux/AppArmor status, etc.