# DERRICK - Leak & CVE Scanner Tool

## Overview

DERRICK is a powerful utility designed to scan and retrieve information about database leaks and CVE (Common Vulnerabilities and Exposures) advisories. It provides a user-friendly interface to search for leaked databases and security vulnerabilities, making it an essential tool for security researchers, penetration testers, and IT professionals.

### The tool consists of two main components:
- **Leak Scanner**: Scans forums like BreachForums for leaked databases.
- **CVE Scanner**: Fetches CVE advisories from the GitHub Security Advisories API.

The tool is built using Python and leverages the `rich` library for a visually appealing command-line interface.

## Features

### Leak Scanner:
- Scans BreachForums for leaked databases.
- Allows filtering by date and keywords.
- Displays results with titles, URLs, and dates.

### CVE Scanner:
- Fetches CVE advisories from the GitHub Security Advisories API.
- Allows filtering by severity, date range, and keywords.
- Displays detailed information about each CVE, including CVSS scores and references.

### User-Friendly Interface:
- Interactive menu for easy navigation.
- Colorful and informative output using the `rich` library.

## Prerequisites

Before using the tool, you need the following:

### GitHub Token:
- A GitHub token is required to access the GitHub Security Advisories API.
- You can generate a token from your GitHub account settings.
- Replace the `GITHUB_TOKEN` in `CVE_Advisories.sh` with your own token.

### BreachForums Cookies:
- To access BreachForums, you need to provide a `cookies.txt` file.
- This file should contain your session cookies from BreachForums.
- You can export cookies using browser extensions like "EditThisCookie" for Chrome or "Cookie-Editor" for Firefox.
- Save the cookies in a file named `cookies.txt` in the root directory of the project.

## Installation

### Clone the Repository:
```bash
git clone https://github.com/supdevinci/derrick.git
cd derrick
```

### Install Dependencies:
```bash
pip install -r requirements.txt
```

### Set Up GitHub Token:
Replace the `GITHUB_TOKEN` in `CVE_Advisories.sh` with your own GitHub token.

Alternatively, you can update the token using the `--add-token` option:
```bash
./CVE_Advisories.sh --add-token=your_github_token
```

### Add BreachForums Cookies:
Export your BreachForums cookies and save them in a file named `cookies.txt` in the root directory.

## Usage

When you run the tool, you will be presented with the main menu:

```
 
 
 
                ██████╗ ███████╗██████╗ ██████╗ ██╗ ██████╗██╗  ██╗
                ██╔══██╗██╔════╝██╔══██╗██╔══██╗██║██╔════╝██║ ██╔╝
                ██║  ██║█████╗  ██████╔╝██████╔╝██║██║     █████╔╝ 
                ██║  ██║██╔══╝  ██╔══██╗██╔══██╗██║██║     ██╔═██╗ 
                ██████╔╝███████╗██║  ██║██║  ██║██║╚██████╗██║  ██╗
                ╚═════╝ ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝ ╚═════╝╚═╝  ╚═╝
                The Ultimate LEAKED Tool v1.0
                   


             Brute Force? Ich monitor! Du still use 'admin123'.
  |████████)    /
  |█|█   __|                      
  |█||--|/.))                       
  (█     ‾ ‾)                      
  |        |                     
  ''..   |_)                    
  |'..'---_      ,____,              
 /    ''---|    //'             
/     \    \ ‾‾ ~               
|  \   \    \
                  
    


Select an option:
[1] Scan database leaks  |  [2] Scan CVE Advisories  |  [q] Quit


Enter your choice  [1/2/q] (1):
```

### 1. Scan Database Leaks
- Option 1: Scan for leaked databases.
- You will be prompted to enter the number of days to search back and a query (optional).

Example:
```bash
Enter number of days for the search [5]: 7
Enter query (leave empty for all leaks): France
```

### 2. Scan CVE Advisories
- Option 2: Scan for CVE advisories.
- You will be prompted to enter the severity level, number of days to search back, and a query (optional).

Example:
```bash
Enter severity level (default: critical): critical
Enter number of days for the search (-d value) [5]: 7
Enter query (leave empty for all advisories): Apache
```

## Contributing
Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## License
This project is licensed under the **MIT License**. See the LICENSE file for details.

## Acknowledgments
- **BreachForums** for the leaked database information.
- **GitHub Security Advisories** for the CVE data.
- **Rich** for the beautiful terminal formatting.
- **Inspecteur Derrick** for the inspiration and the iconic detective vibes.

> **Note:** This tool is intended for **educational and research purposes only**. Use it responsibly and ensure you have permission to scan and access any resources.
