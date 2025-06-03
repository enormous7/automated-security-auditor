# automated-security-auditor
Automated system security auditing and reporting tools

-----

# 🛡️ Automated System Security Auditor

This repository hosts a Python-based tool designed to **automate the process of auditing core operating system security configurations, identifying potential vulnerabilities, and generating comprehensive security reports**. For information system security professionals, routine security checks, efficient issue management, and compliance verification are paramount. This solution streamlines these repetitive auditing tasks, significantly reducing manual effort and ensuring a consistent, systematic approach to security assessments.

### Demonstrating Core Competencies for an Information System Security Specialist

This project specifically addresses the critical competencies sought in an **Information System Security Specialist** role. It serves as a testament to my sustained engagement and practical skill development in the security domain, particularly during my career transition.

  * **Vulnerability Analysis & Security Auditing:** Demonstrates proficiency in evaluating diverse system security settings and identifying common vulnerabilities.
  * **Automation & Efficiency:** Highlights the ability to design and implement automated solutions for repetitive security tasks, thereby maximizing operational efficiency.
  * **Problem Solving & Reporting:** Showcases strong analytical skills in interpreting audit findings, pinpointing security weaknesses, and producing clear, actionable reports for effective communication.
  * **Commitment to Continuous Learning:** The outlined future enhancements reflect a proactive approach to adapting to evolving security landscapes and integrating new technologies.

-----

## 🚀 Key Features

  * **Operating System Baseline Security Checks:**
      * Verification of password policy adherence (e.g., minimum length, complexity).
      * Confirmation of disabled direct root login via SSH.
      * Detection of user accounts lacking password protection.
  * **Service and Network Security Assessment:**
      * Identification of unnecessarily running services.
      * Discovery of listening ports and associated process information.
  * **File and Directory Permission Auditing:**
      * Validation of appropriate permissions for critical system files (e.g., `/etc/passwd`, `/etc/shadow`, `/etc/sudoers`, `/etc/ssh/sshd_config`).
      * Detection of files or directories with overly permissive (e.g., `777`) permissions.
      * Identification of files with SetUID/SetGID bits set, indicating potential privilege escalation vectors.
  * **Versatile Report Generation:**
      * Automated output of audit results in **JSON, Markdown, and Plain Text** formats.
      * Reports include both high-level summaries and detailed findings.

-----

## 🛠️ Setup and Execution

### Prerequisites

  * **Python 3.8+**
  * **Git** (Installation guides available on the [Git official website](https://git-scm.com/downloads)).
  * **Linux Operating System** (Currently optimized for Linux environments).

### Installation

1.  **Clone the Repository:**

    ```bash
    git clone https://github.com/<YOUR_GITHUB_USERNAME>/automated-security-auditor.git
    cd automated-security-auditor
    ```

2.  **Install Dependencies:**
    (Although currently relying on built-in Python libraries, this step is essential for future expansions.)

    ```bash
    pip install -r requirements.txt
    ```

### Running the Audit

Certain security checks require elevated privileges to access system files or execute commands. It is **recommended to run the script with `sudo`**:

```bash
python3 main.py
```

or

```bash
sudo python3 main.py
```

Upon completion, audit reports (e.g., `security_audit_report_YYYYMMDD_HHMMSS.json`, `.md`, `.txt`) will be generated in the current directory.

-----

## 📁 Project Structure

```
automated-security-auditor/
├── .gitignore
├── LICENSE
├── README.md                 # Comprehensive project documentation
├── main.py                   # Orchestrates audit execution and report generation
├── security_checks/          # Contains modular security check functions
│   ├── __init__.py
│   ├── os_checks.py          # Focuses on OS-level security configurations
│   ├── service_checks.py     # Examines running services for security posture
│   └── file_permission_checks.py # Audits file and directory access permissions
├── config.py                 # Centralized configuration for audit parameters
├── report_generator.py       # Manages the formatting and output of audit reports
├── requirements.txt          # Lists all project dependencies
└── tests/                    # (Optional) Future directory for unit and integration tests
```

-----

## 📈 Future Enhancements and Expansion

  * **Windows OS Compatibility:** Extend auditing capabilities to Windows environments, including checks for Registry security, Group Policies, and Windows Defender status.
  * **Advanced Network Security Auditing:** Incorporate deeper analysis of firewall rules (UFW/iptables, Windows Firewall) and identification of vulnerable network protocols.
  * **Vulnerability Database Integration:** Integrate with industry-standard vulnerability databases (e.g., CVE) for enhanced threat identification.
  * **Interactive Report Visualization:** Develop capabilities for generating interactive HTML dashboards or graphical reports to provide clearer insights.
  * **Automated Scheduling:** Implement a scheduling mechanism for recurring security audits.
  * **Configuration Management Tool Integration:** Facilitate integration with tools like Ansible, Chef, or Puppet for automated security hardening and remediation.
  * **Cloud Security Posture Management:** Expand to audit security configurations within cloud platforms (e.g., AWS, Azure, GCP).

-----

## 📄 License

This project is released under the **MIT License**. Refer to the `LICENSE` file for full details.

-----

Developed by enormous7 (https://www.google.com/search?q=https://github.com/enormous7)
