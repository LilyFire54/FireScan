"""
🛡️ FireScan — Custom Port Scanner
Author: FireLily (Kayla M.)

DISCLAIMER:
This tool is intended for educational purposes and personal portfolio demonstration only.
Unauthorized scanning of systems or networks without explicit permission is illegal and unethical.
Use this tool responsibly and in compliance with all applicable laws and regulations.
The author assumes no responsibility for any misuse or damage caused by this tool.

By using FireScan, you agree to these terms.
"""

import socket
from datetime import datetime
from tqdm import tqdm
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

def scan_ports(target, port_range=(1, 1024), export=False):
    print(f"\n{Fore.CYAN}[🔥 FireScan] Scanning {target} from port {port_range[0]} to {port_range[1]}")
    print(f"Scan started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")

    open_ports = []

    try:
        ports = range(port_range[0], port_range[1] + 1)
        for port in tqdm(ports, desc="Scanning Ports", unit="port"):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1.5)  # Increased timeout
            result = sock.connect_ex((target, port))
            if result == 0:
                try:
                    banner = sock.recv(1024).decode().strip()
                except:
                    banner = "No banner"
                port_info = f"Port {port} - {banner}"
                print(f"{Fore.GREEN}[OPEN] {port_info}")
                open_ports.append(port_info)
            sock.close()

        if export and open_ports:
            filename = f"scan_results_{target.replace('.', '_')}.txt"
            with open(filename, 'w') as f:
                f.write(f"FireScan Results for {target}\n")
                f.write(f"Scan Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                for entry in open_ports:
                    f.write(f"[OPEN] {entry}\n")
            print(f"\n{Fore.YELLOW}Scan results exported to {filename}")

    except KeyboardInterrupt:
        print(f"\n{Fore.RED}[!] Scan cancelled by user.")
    except socket.gaierror:
        print(f"\n{Fore.RED}[!] Hostname could not be resolved.")
    except socket.error:
        print(f"\n{Fore.RED}[!] Could not connect to server.")

if __name__ == "__main__":
    target = input("Enter target IP or hostname: ")
    save = input("Do you want to export the results to a file? (y/n): ").lower() == 'y'
    scan_ports(target, export=save)