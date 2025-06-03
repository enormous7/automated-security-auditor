# main.py

import os
import subprocess
from security_checks import os_checks, service_checks, file_permission_checks
from report_generator import generate_report, save_report
from config import TARGET_OS # Currently only Linux is supported

def run_all_checks():
    """
    Executes all defined security checks and collects the results.
    """
    audit_results = []

    print("--- Starting System Security Audit ---")

    if TARGET_OS == "Linux":
        print("\n[OS Basic Security Checks]")
        audit_results.append(os_checks.check_password_policy())
        audit_results.append(os_checks.check_root_login_ssh())
        audit_results.append(os_checks.check_empty_passwords())

        print("\n[Service Security Checks]")
        audit_results.append(service_checks.check_running_services())
        audit_results.append(service_checks.check_open_ports())

        print("\n[File and Directory Permission Checks]")
        # Sensitive file permission checks
        audit_results.extend(file_permission_checks.check_sensitive_file_permissions(
            ["/etc/passwd", "/etc/shadow", "/etc/sudoers", "/etc/ssh/sshd_config"]))
        
        # Full file system permission check (Caution: can take a long time, run only if needed)
        # This check scans the '/' path and may require `sudo` privileges. It can be very time-consuming.
        # For initial testing, it's recommended to comment it out or limit it to a smaller path.
        print("  Warning: Full file system permission check may take a long time.")
        print("  Root privileges might be required. (Can be interrupted with Ctrl+C)")
        # audit_results.extend(file_permission_checks.traverse_and_check_permissions(base_path='/'))
        # To enable the commented line above, uncomment it and run with `sudo` if necessary.
        # Example for checking only the `/tmp` directory:
        # audit_results.extend(file_permission_checks.traverse_and_check_permissions(base_path='/tmp'))

    else:
        print(f"Unsupported operating system: {TARGET_OS}")
        audit_results.append({"name": "OS Support", "status": "ERROR", "details": f"{TARGET_OS} is not currently supported."})

    print("\n--- System Security Audit Completed ---")
    return audit_results

if __name__ == "__main__":
    # Check script execution permissions (root privileges may be required)
    if os.geteuid() != 0:
        print("Warning: Some security checks require root privileges. It is recommended to run with 'sudo python3 main.py'.")

    results = run_all_checks()
    
    # Generate and save reports
    # JSON format report
    json_report_content = generate_report(results, report_format="json")
    save_report(json_report_content, filename="security_audit_report", report_format="json")

    # Markdown format report (easy to add to GitHub README)
    markdown_report_content = generate_report(results, report_format="markdown")
    save_report(markdown_report_content, filename="security_audit_report", report_format="md")

    # Text format report (for quick review)
    text_report_content = generate_report(results, report_format="text")
    save_report(text_report_content, filename="security_audit_report", report_format="txt")

    print("\nAll audits and report generation completed.")
    print("Please check the generated report files.")