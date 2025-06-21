## 💡 Background & Use Case

This repository contains **handcrafted scripts and workarounds** I used while working on the **Dante Pro Lab** (from Hack The Box).

> ⚠️ **Note**: This is **not a spoiler**. You can find similar solutions online, but the automation and execution logic here are custom-built and battle-tested. Trust me — once you use them, you’ll thank yourself later.

---

### 😖 Pain Point: Repeated Tunneling

One of the biggest time-wasters was **setting up tunnels repeatedly** after each reset or re-attempt. To solve this, I built a **one-shot pivot script (`auto-pivot.py`)** that:

1. Connects to the compromised host via SSH.
2. Downloads the **Chisel client** using `wget`.
3. Makes it executable and runs it with the appropriate reverse tunnel arguments.
4. Drops you straight into an **interactive SSH shell** on the target.

---

### ⚙️ Prerequisites for `auto-pivot.py`

Before running the script:

1. **Host the Chisel binary** on your attacking machine:

   ```bash
   python3 -m http.server 8081
   ```

   > You can change the port from `8081` to any available one, but **make sure to update it in the script as well**.

2. **Start the Chisel server** on your machine:

   ```bash
   ./chisel server -p 8000 --reverse
   ```

Once done, run the script:

```bash
python3 auto-pivot.py
```

> This will connect to the target, fetch Chisel, set it up with reverse tunneling, and leave you inside a working shell — all in one go.



### 🧠 Reminder: Set up ProxyChains

Make sure to configure your proxy to route traffic through the newly created SOCKS tunnel:

```bash
sudo nano /etc/proxychains4.conf
```

Add the following line (if not already present):

```bash
socks5 127.0.0.1 1080
```

Then you can access internal services like:

```bash
proxychains -q nxc smb 172.16.x.0/24
```

---

## 🛠️ SSH Config Fixer Script (`ssh_config_fixer.py`)

When trying to use SSH utilities from within a compromised system, you might encounter errors like:

```
/etc/ssh/ssh_config: line 53: Bad configuration option: denyusers
/etc/ssh/ssh_config: line 54: Bad configuration option: permitrootlogin
/etc/ssh/ssh_config: terminating, 2 bad configuration options
```

These errors occur because `DenyUsers` and `PermitRootLogin` are invalid in the **SSH client config** (`ssh_config` instead of `sshd_config`).

To avoid manually editing via `nano` (which often breaks interactive shells), I wrote a quick fix script:

```bash
sudo python3 ssh_config_fixer.py
```

✅ **Expected Output:**

```
[+] Backing up original config...
[+] Parsing and fixing ssh_config...
[+] Done. Invalid options have been commented out.
[!] A backup was saved at: /etc/ssh/ssh_config.bak
```

Once done, you should be able to use SSH commands without config-related crashes.

Finally One run. One pivot. Total control.

Now go pop those internal boxes.
And hey — don’t forget to star ⭐ the repo if it saved your ass. 😉
