# ARP Spoofer (Lab-Only, Educational)

> **⚠ Legal & Ethical Notice**
> This project is for **authorized, lab-only** security research and education. **Do not** run it against any network without **written permission** from its owner. Misuse may violate laws and institutional policies. The author is not responsible for any misuse or damage.

## Overview

A simple **ARP spoofer** written in Python with **Scapy**. It poisons the ARP caches of a victim and a router, places the attacker machine in the middle of their traffic (a man-in-the-middle position), and forwards the intercepted packets to their real destination so connectivity keeps working transparently.

Built as part of a cybersecurity course, for learning purposes only and tested in an isolated lab environment.

### How It Works

```
Victim  <——(spoofed ARP)——  Attacker  ——(forwarded traffic)——>  Router/Internet
            ^                      |
            |——(spoofed ARP)———–——|
```

1. **ARP poisoning** — a background thread continuously sends forged ARP replies (`op=2`) to the victim and to the router, each telling the other machine that the attacker's MAC belongs to its counterpart's IP.
2. **Sniffing** — the main thread sniffs all IP traffic on the chosen interface.
3. **Forwarding** — every intercepted packet is re-sent to its real destination by rewriting the Ethernet source/destination MACs, so the victim's connection keeps working while the attacker sees the traffic.

## Requirements

* Linux
* Python 3
* [Scapy](https://scapy.net/) — `pip install scapy`
* Root privileges (raw sockets)

## Configuration

Before running, open `arp_spoofer.py` and set these values for your own lab network:

```python
victim_ip  = "10.10.1.x"       # IP of the victim machine
router_ip  = "10.10.0.x"       # IP of the router / default gateway
victim_mac = "aa:bb:cc:dd:ee:ff"   # MAC of the victim machine
router_mac = "aa:bb:cc:dd:ee:ff"   # MAC of the router
interface  = "wlp0s20f3"       # Your network interface (see `ip addr`)
```

* Use `ip addr` to find your interface name.
* Use `arp -a` (or `ip neigh`) to look up the victim's and router's MAC addresses.

> These values **must** be changed to match your environment, otherwise the tool won't work.

## Usage

Run with root privileges:

```bash
sudo python3 arp_spoofer.py
```

Stop with `Ctrl + C`.

## Validating Behavior

> Run only on an isolated test network or virtual lab.

* **Ping (ICMP):** run `ping` from the victim toward the router or the internet, and capture packets on the attacker with Wireshark. The victim should still get replies, while the attacker sees the ICMP traffic passing through.
* **Unencrypted transfer:** send a plain-text file between the victim and another host and confirm the attacker can observe it in Wireshark while the transfer still completes.

## Limitations & Possible Improvements

* **MAC resolution is manual** — the victim and router MACs are hardcoded. A future version could resolve them automatically with ARP requests.
* **No ARP restore on exit** — the spoofed ARP entries stay in the caches until they time out or the machines are refreshed. A cleanup step that re-sends the correct ARP mappings on exit would make the attack cleaner to tear down.
* IP forwarding is handled in user space by this script, so kernel IP forwarding should stay disabled.
