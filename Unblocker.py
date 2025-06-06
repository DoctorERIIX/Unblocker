import os
import shutil
import time
import sys
from datetime import datetime
from colorama import init, Fore
import ctypes
from ctypes import wintypes

# Initialize colorama
init()

# Constants for Windows API
GWL_STYLE = -16
WS_MINIMIZEBOX = 0x00020000
WS_MAXIMIZEBOX = 0x00010000
WS_SIZEBOX = 0x00040000
SWP_NOSIZE = 0x0001
SWP_NOMOVE = 0x0002
SWP_NOZORDER = 0x0004
SWP_FRAMECHANGED = 0x0020

def set_window_properties():
    try:
        # Get console window handle
        hwnd = ctypes.windll.kernel32.GetConsoleWindow()
        
        # Set the title of the window to "TeamSpeak Unblocker"
        ctypes.windll.kernel32.SetConsoleTitleW("TeamSpeak Unblocker")
        
        # Disable minimize, maximize, and resize
        style = ctypes.windll.user32.GetWindowLongW(hwnd, GWL_STYLE)
        style &= ~WS_MINIMIZEBOX
        style &= ~WS_MAXIMIZEBOX
        style &= ~WS_SIZEBOX
        ctypes.windll.user32.SetWindowLongW(hwnd, GWL_STYLE, style)
        
        # Update the window to apply changes
        ctypes.windll.user32.SetWindowPos(
            hwnd, 0, 0, 0, 0, 0,
            SWP_NOMOVE | SWP_NOSIZE | SWP_NOZORDER | SWP_FRAMECHANGED
        )
        
        return True
    except Exception as e:
        print(f"[-] Error setting window properties: {e}")
        return False

def set_window_size(width, height):
    os.system(f'mode con: cols={width} lines={height}')
    set_window_properties()  # Apply window modifications after resizing

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    clear_screen()
    print(Fore.BLUE + r"""
██╗   ██╗███╗   ██╗██████╗ ██╗      ██████╗  ██████╗██╗  ██╗███████╗██████╗ 
██║   ██║████╗  ██║██╔══██╗██║     ██╔═══██╗██╔════╝██║ ██╔╝██╔════╝██╔══██╗
██║   ██║██╔██╗ ██║██████╔╝██║     ██║   ██║██║     █████╔╝ █████╗  ██████╔╝
██║   ██║██║╚██╗██║██╔══██╗██║     ██║   ██║██║     ██╔═██╗ ██╔══╝  ██╔══██╗
╚██████╔╝██║ ╚████║██████╔╝███████╗╚██████╔╝╚██████╗██║  ██╗███████╗██║  ██║
 ╚═════╝ ╚═╝  ╚═══╝╚═════╝ ╚══════╝ ╚═════╝  ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
                                                                            
""")
    print(Fore.LIGHTBLUE_EX + "[!] TeamSpeak Unblocker | Discord : eriix.me" + Fore.RESET)

def loading_animation():
    print(Fore.GREEN + "[+] Processing..." + Fore.RESET)
    for i in range(10):
        time.sleep(0.2)
        sys.stdout.write(Fore.GREEN + ' •' + Fore.RESET)
        sys.stdout.flush()

def modify_hosts_file():
    hosts_path = r"C:\Windows\System32\drivers\etc\hosts"
    backup_base_path = r"C:\Windows\System32\drivers\etc\hosts_backup"
    
    entries_to_add = [
        "127.0.0.1 blacklist.teamspeak.com",
        "127.0.0.1 blacklist2.teamspeak.com"
    ]
    
    try:
        if not os.path.exists(hosts_path):
            print(Fore.RED + "[-] Hosts file not found!" + Fore.RESET)
            return False
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = f"{backup_base_path}_{timestamp}"
        shutil.copy2(hosts_path, backup_path)
        print(Fore.GREEN + f"\n[+] Backup created:{backup_path}" + Fore.RESET)
        
        with open(hosts_path, 'r', encoding='utf-8') as file:
            content = file.readlines()
        
        if any(entry in [line.strip() for line in content if line.strip() and not line.startswith('#')] for entry in entries_to_add):
            print(Fore.GREEN + "[+] Entries already exist in hosts file." + Fore.RESET)
            return True
        
        with open(hosts_path, 'a', encoding='utf-8') as file:
            file.write("\n# Added by TeamSpeak unblock script\n")
            for entry in entries_to_add:
                file.write(entry + "\n")
        
        return True
    
    except PermissionError:
        print(Fore.RED + "\n[-] Error: Permission denied. Please run as Administrator." + Fore.RESET)
        return False
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

if __name__ == "__main__":
    # Set window size to 77x29 and lock it
    set_window_size(77, 29)
    
    # Print banner and run main program
    print_banner()
    input(Fore.BLUE + "[>] Press ENTER to continue..." + Fore.RESET)
    loading_animation()
    
    if modify_hosts_file():
        print(Fore.GREEN + "[+] Operation completed successfully!" + Fore.RESET)
        print(Fore.GREEN + "[+] TeamSpeak blacklist has been blocked successfully." + Fore.RESET)
    else:
        print(Fore.RED + "[-] Operation failed!" + Fore.RESET)
        print(Fore.RED + "[-] Please check the error messages above." + Fore.RESET)
    
    # Keep window open until user presses ENTER
    input(Fore.BLUE + "[>] Press ENTER to exit..." + Fore.RESET)