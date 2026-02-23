import warnings
from cryptography.utils import CryptographyDeprecationWarning
warnings.filterwarnings("ignore", category=CryptographyDeprecationWarning)

from scapy.all import sniff, wrpcap
import os

PACKETS_TO_CAPTURE = 1000
CAPTURE_FILE_PREFIX = "captured_packets"

# ===== PATH FIX (LOCAL + DOCKER SUPPORT) =====
if os.path.exists("/app"):
    BASE_PATH = "/app/data1"        # Docker path
else:
    BASE_PATH = os.getcwd()         # Your laptop folder

PCAP_FILE = os.path.join(BASE_PATH, "captured_traffic.pcap")
# ============================================

captured_packets = []

# Function to capture packets
def packet_callback(packet):
    global captured_packets
    captured_packets.append(packet)

    if len(captured_packets) == PACKETS_TO_CAPTURE:
        save_packets()

def save_packets():
    global captured_packets
    wrpcap(PCAP_FILE, captured_packets)
    print(f"{len(captured_packets)} packets captured and saved to {PCAP_FILE}")
    captured_packets = []

def main():
    print("Starting packet capture...")
    sniff(prn=packet_callback, store=0)

if __name__ == "__main__":
    main()
