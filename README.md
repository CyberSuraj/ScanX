# 🔍 ScanX – Fast Port Scanner

**ScanX** is a multi‑threaded port scanner that checks for open ports on a range of IP addresses.  
It automatically saves results to `/sdcard/ScanX/` (on Android) or the current directory on other systems.

![Python](https://img.shields.io/badge/Python-3.7%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)

## ✨ Features

- Scan **single port** (e.g., `443`) or **multiple ports** (e.g., `80,8080,443,22`)
- **Only open ports** are displayed (clean output)
- Results saved automatically in a `.txt` file
- Coloured terminal output (IP in green, HTTP in red)
- Supports **Ctrl+C** – clean exit with `Exiting...` message
- Works on **Termux**, **Kali Linux**, **Ubuntu**, **Windows**, **macOS**

## 🚀 Installation & Usage

All commands are listed as bullet points with `*`.

### 1. Clone the repository

* `git clone https://github.com/CyberSuraj/ScanX.git`
* `cd ScanX`

### 2. Install required Python packages

* `pip install requests colorama pyfiglet ipaddress`

### 3. Run the tool

* `python ScanX.py`

## 🖥️ Platform‑Specific Commands

### 📱 Termux (Android)

* `pkg update && pkg upgrade`
* `pkg install python git`
* `git clone https://github.com/CyberSuraj/ScanX.git`
* `cd ScanX`
* `pip install requests colorama pyfiglet ipaddress`
* `python ScanX.py`

> **Note:** Results are saved to `/sdcard/ScanX/`. Grant storage permission:  
> `termux-setup-storage`

### 🐧 Kali Linux / Ubuntu / Debian

* `sudo apt update`
* `sudo apt install python3 python3-pip git`
* `git clone https://github.com/CyberSuraj/ScanX.git`
* `cd ScanX`
* `pip3 install requests colorama pyfiglet ipaddress`
* `python3 ScanX.py`

### 🪟 Windows

* `git clone https://github.com/CyberSuraj/ScanX.git`
* `cd ScanX`
* `pip install requests colorama pyfiglet ipaddress`
* `python ScanX.py`

### 🍎 macOS

* `brew install python git`   (if Homebrew is installed)
* `git clone https://github.com/CyberSuraj/ScanX.git`
* `cd ScanX`
* `pip3 install requests colorama pyfiglet ipaddress`
* `python3 ScanX.py`

## 📝 How to Use

1. Run the tool: `python ScanX.py`
2. Enter **Start IP** and **End IP** (e.g., `192.168.1.1` and `192.168.1.10`)
3. Enter **ports** to scan:
   - Single port: `443`
   - Multiple ports: `80,8080,443,22`
   - Press **Enter** to use default ports `80,8080`
4. The scan starts immediately. Only **open ports** will be shown.
5. After the scan, results are saved to `/sdcard/ScanX/startIP_to_endIP.txt` (or `./ScanX/` on non‑Android).
6. Press **Enter** to clear the screen and start a new scan.
7. Press **Ctrl+C** at any time to exit cleanly.

## 📂 Example Output
<img width="1237" height="1280" alt="1000017734" src="https://github.com/user-attachments/assets/cca45f0e-8cba-447e-8f07-e5cd69e8d0a4" />


## 🤝 Contributing

Feel free to fork this repository, open issues, or submit pull requests.

## 📜 License

This project is completely open.  
✅ Anyone can use, modify, or redistribute this code.  
✅ You can build your own script based on it.  
✅ No restrictions – full permission granted.

## 👨‍💻 Author

**CyberSuraj**  
[GitHub: @CyberSuraj](https://github.com/CyberSuraj)

---

⭐ Don’t forget to star the repository if you found it useful!
