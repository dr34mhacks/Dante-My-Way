import os
import shutil

SSH_CONFIG = "/etc/ssh/ssh_config"
BACKUP_CONFIG = "/etc/ssh/ssh_config.bak"
BAD_OPTIONS = ["DenyUsers", "PermitRootLogin"]

def main():
    # Ensure we run as root
    if os.geteuid() != 0:
        print("[-] This script must be run as root (use sudo).")
        return

    print("[+] Backing up original config...")
    shutil.copy(SSH_CONFIG, BACKUP_CONFIG)

    print("[+] Parsing and fixing ssh_config...")
    fixed_lines = []
    with open(SSH_CONFIG, "r") as f:
        for line in f:
            stripped = line.strip()
            if any(stripped.lower().startswith(opt.lower()) for opt in BAD_OPTIONS):
                fixed_lines.append(f"# {line}" if not line.lstrip().startswith("#") else line)
            else:
                fixed_lines.append(line)

    with open(SSH_CONFIG, "w") as f:
        f.writelines(fixed_lines)

    print("[+] Done. Invalid options have been commented out.")
    print(f"[!] A backup was saved at: {BACKUP_CONFIG}")

if __name__ == "__main__":
    main()

