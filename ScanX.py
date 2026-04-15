import socket
import requests
import time
import threading
from queue import Queue
import ipaddress
from colorama import Fore, Style
import pyfiglet
from datetime import datetime
import os
import sys

socket.setdefaulttimeout(0.25)
lock = threading.Lock()
scan_results = []

def get_public_ip():
    try:
        response = requests.get('https://api.ipify.org', timeout=3)
        if response.status_code == 200:
            return response.text
        return "Unknown"
    except:
        return "Unknown"

def get_country(ip):
    try:
        response = requests.get(f'http://ip-api.com/json/{ip}', timeout=3)
        if response.status_code == 200:
            data = response.json()
            return data.get('country', 'Unknown')
        return "Unknown"
    except:
        return "Unknown"

def scan(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        con = sock.connect((ip, port))
        with lock:
            if port == 8080:
                msg = f"Port {port} is open on {Fore.GREEN}{ip}{Style.RESET_ALL}:{port} {Fore.RED}HTTP{Style.RESET_ALL}"
            else:
                msg = f"Port {port} is open on {Fore.GREEN}{ip}{Style.RESET_ALL}"
            print(msg)
            scan_results.append(f"{ip}:{port}" + (" (HTTP)" if port == 8080 else ""))
        con.close()
    except:
        pass

def execute(queue):
    while True:
        ip, port = queue.get()
        scan(ip, port)
        queue.task_done()

def generate_ip_range(start_ip, end_ip):
    try:
        start = int(ipaddress.IPv4Address(start_ip))
        end = int(ipaddress.IPv4Address(end_ip))
        for ip_int in range(start, end + 1):
            yield str(ipaddress.IPv4Address(ip_int))
    except:
        return

def print_logo():
    cyan = Fore.CYAN
    yellow = Fore.YELLOW
    magenta = Fore.MAGENTA
    reset = Style.RESET_ALL

    logo = pyfiglet.figlet_format("ScanX", font="slant")
    logo_lines = logo.split('\n')
    
    pub_ip = get_public_ip()
    country = get_country(pub_ip)
    current_time = datetime.now().strftime('%Y-%m-%d %I:%M:%S %p')
    
    print(f"{cyan}{'='*60}{reset}")
    for line in logo_lines:
        if line.strip():
            print(f"{cyan}{line.center(60)}{reset}")
    print(f"{cyan}{'-'*60}{reset}")
    print(f"{yellow}IP: {pub_ip}  |  Country: {country}  |  Time: {current_time}{reset}")
    print(f"{magenta}GitHub: @CyberSuraj{reset}")
    print(f"{cyan}{'='*60}{reset}\n")

def save_results_to_file(start_ip, end_ip, ports_scanned):
    save_dir = "/sdcard/ScanX"
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    filename = f"{start_ip}_to_{end_ip}.txt"
    filepath = os.path.join(save_dir, filename)
    with open(filepath, 'w') as f:
        f.write(f"ScanX Scan Report\n")
        f.write(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"IP Range: {start_ip} - {end_ip}\n")
        f.write(f"Ports scanned: {', '.join(map(str, ports_scanned))}\n")
        f.write("-" * 50 + "\n")
        if scan_results:
            for res in scan_results:
                f.write(res + "\n")
        else:
            f.write("No open ports found.\n")
        f.write("-" * 50 + "\n")
        f.write(f"Total open ports: {len(scan_results)}\n")
    print(f"\n{Fore.GREEN}[✓] Results saved to: {filepath}{Style.RESET_ALL}")

def clear_screen():
    os.system('clear' if os.name != 'nt' else 'cls')

def run_tool():
    global scan_results
    while True:
        clear_screen()
        print_logo()
        
        # Input Start IP with validation
        while True:
            start_ip = input('Start IP Address: ').strip()
            if not start_ip:
                print(f"{Fore.RED}Error: Start IP cannot be empty. Please enter a valid IP.{Style.RESET_ALL}")
                continue
            try:
                ipaddress.IPv4Address(start_ip)
                break
            except:
                print(f"{Fore.RED}Error: Invalid IP address format. Try again.{Style.RESET_ALL}")
        
        # Input End IP with validation
        while True:
            end_ip = input('End IP Address: ').strip()
            if not end_ip:
                print(f"{Fore.RED}Error: End IP cannot be empty. Please enter a valid IP.{Style.RESET_ALL}")
                continue
            try:
                ipaddress.IPv4Address(end_ip)
                # Check if end IP is >= start IP
                if int(ipaddress.IPv4Address(end_ip)) >= int(ipaddress.IPv4Address(start_ip)):
                    break
                else:
                    print(f"{Fore.RED}Error: End IP must be greater than or equal to Start IP.{Style.RESET_ALL}")
            except:
                print(f"{Fore.RED}Error: Invalid IP address format. Try again.{Style.RESET_ALL}")
        
        # Port input (empty allowed -> default)
        port_input = input('Enter ports (e.g., 443 or 80,8080,443) [Enter for default 80,8080]: ').strip()
        if port_input == "":
            ports_to_scan = [80, 8080]
            print(f"{Fore.CYAN}Using default ports: 80, 8080{Style.RESET_ALL}")
        else:
            try:
                ports_to_scan = [int(p.strip()) for p in port_input.split(',')]
                if len(ports_to_scan) == 1:
                    print(f"{Fore.CYAN}Scanning single port: {ports_to_scan[0]}{Style.RESET_ALL}")
                else:
                    print(f"{Fore.CYAN}Scanning multiple ports: {', '.join(map(str, ports_to_scan))}{Style.RESET_ALL}")
            except ValueError:
                print(f"{Fore.RED}Invalid port input. Using default 80,8080.{Style.RESET_ALL}")
                ports_to_scan = [80, 8080]
        
        scan_results = []
        queue = Queue()
        start_time = time.time()
        
        # Start threads
        for _ in range(100):
            t = threading.Thread(target=execute, args=(queue,))
            t.daemon = True
            t.start()
        
        # Feed jobs
        for ip in generate_ip_range(start_ip, end_ip):
            for port in ports_to_scan:
                queue.put((ip, port))
        
        queue.join()
        elapsed = time.time() - start_time
        print(f'\n{Fore.YELLOW}Time taken: {elapsed:.2f} seconds{Style.RESET_ALL}')
        
        if scan_results:
            save_results_to_file(start_ip, end_ip, ports_to_scan)
        else:
            print(f"\n{Fore.RED}No open ports found. Nothing to save.{Style.RESET_ALL}")
        
        input(f"\n{Fore.CYAN}Press Enter to clear screen and start a new scan...{Style.RESET_ALL}")

if __name__ == "__main__":
    try:
        run_tool()
    except KeyboardInterrupt:
        print(f"\n\n{Fore.RED}Exiting...{Style.RESET_ALL}")
        sys.exit(0)
