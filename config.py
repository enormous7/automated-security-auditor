# config.py

# Target operating system for audit
# Currently focused on Linux, but can be configured for future expansion
TARGET_OS = "Linux"

# Directories to exclude from checks (e.g., large log file directories)
EXCLUDE_DIRS = [
    "/proc",
    "/sys",
    "/dev",
    "/run",
    "/tmp",
    "/var/lib",
    "/var/cache",
    "/var/log" # Exclude as log files can be extensive and slow down scans
]

# Minimum password length for password policy checks
MIN_PASSWORD_LENGTH = 8

# SSH configuration file path (e.g., /etc/ssh/sshd_config)
SSH_CONFIG_PATH = "/etc/ssh/sshd_config"

# List of unnecessary services (examples)
UNNECESSARY_SERVICES = [
    "telnet",
    "ftp",
    "vsftpd" # Example, add more based on your environment
]