import random
import subprocess
import os
from datetime import datetime, timedelta
from rich.console import Console
from rich.prompt import Prompt
from rich.progress import Progress, BarColumn, TextColumn, TimeElapsedColumn
from rich.table import Table

# Initialisation de la console
console = Console()

# Constantes
VERSION = "v1.0"
DEFAULT_DAYS = 5  # Nombre de jours par défaut

random_phrases = [
    # 🛡️ Leak-related phrases
    "Leak gefunden? Ich trace fast!",
    "Datenbank? Ich browse deep!",
    "Security? Ich break leaks!",
    "Dump gefunden? Ich scan alles!",
    "Passwords? Ich finde schnell!",
    "Darknet? Ich search leaks!",
    "Private keys? Ich expose now!",
    "Hacking? Ich leak info!",
    "Security breach? Ich index sofort!",
    "Daten verloren? Ich recover leaks!",
    "Black market? Ich analyze files!",
    "Secret data? Ich reveal leaks!",
    "Cybercrime? Ich detect sources!",
    "Anonym? Ich track footprints!",
    "Versteckte Dateien? Ich find alles!",
    "Forensik? Ich scrape tief!",
    "Exponiert? Ich search dumps!",
    "Verschlüsselung? Ich break schnell!",
    "Datenleck? Ich check alles!",

    # 🛡️ CVE-related phrases (Mit mehr Englisch & Ironie)
    "Zero-Day? Ich report it! But Du ignore it.",
    "Exploit gefunden? Ich analyze! Du hope it's fake.",
    "Schwachstelle? Ich scan it! Du trust die firewalls.",
    "Ungepatcht? Ich prüfe! Du say 'later'.",
    "Kernel Panic? Ich debug! Du restart and pray.",
    "Remote Code? Ich see it! Du still use die default creds?",
    "Buffer Overflow? Ich finde it! Du don’t care until der crash.",
    "Privilege Escalation? Ich detect! Du say 'not mein problem'.",
    "Patchday? Ich install die updates! Du click 'remind mich tomorrow'.",
    "CVE detected? Ich log it! Du close deine eyes.",
    "Exploit? Ich reverse-engineer! Du google 'how to fix'.",
    "Memory Corruption? Ich debug! Du ask ChatGPT for hilfe.",
    "Injection? Ich find it! Du think 'nobody tries this'.",
    "Brute Force? Ich monitor! Du still use 'admin123'.",
    "APT detected? Ich track! Du think 'we are too small'.",
    "XSS? Ich break it! Du ignore die security headers.",
    "Ransomware? Ich analyze! Du call der boss.",
    "Malware? Ich detect it! Du double-click anyway.",
    "Firewall Bypass? Ich check! Du whitelist everything.",
    "SOC Alert? Ich read die logs! Du delete them.",
]


# Couleur pastel aléatoire
def random_pastel_color():
    r = random.randint(150, 255)
    g = random.randint(150, 255)
    b = random.randint(150, 255)
    return f"rgb({r},{g},{b})"

def display_derrick():
    colors = [random_pastel_color() for _ in range(6)]
    
    ascii_art_lines = [
        " ",
        " ",
        " ",
        "                ██████╗ ███████╗██████╗ ██████╗ ██╗ ██████╗██╗  ██╗",
        "                ██╔══██╗██╔════╝██╔══██╗██╔══██╗██║██╔════╝██║ ██╔╝",
        "                ██║  ██║█████╗  ██████╔╝██████╔╝██║██║     █████╔╝ ",
        "                ██║  ██║██╔══╝  ██╔══██╗██╔══██╗██║██║     ██╔═██╗ ",
        "                ██████╔╝███████╗██║  ██║██║  ██║██║╚██████╗██║  ██╗",
        "                ╚═════╝ ╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝╚═╝ ╚═════╝╚═╝  ╚═╝"
    ]
    
    colored_ascii_art = "\n".join(
        f"[bold {colors[i % len(colors)]}]{line}[/bold {colors[i % len(colors)]}]"
        for i, line in enumerate(ascii_art_lines)
    )
    
    title = f"                [bold cyan]The Ultimate LEAKED Tool[/bold cyan] [bold magenta]{VERSION}[/bold magenta]".center(80) 
    title2 = f"                [bold cyan] [/bold cyan] [bold white] [/bold white]" 
    
    second_ascii_art = r"""

             [bold white]""" + random.choice(random_phrases) + r"""[/bold white]
[bold white]  |████████)    /
  |█|█   __|                      
  |█||--|/.))                       
  (█     ‾ ‾)                      
  |        |                     
  ''..   |_)                    
  |'..'---_      ,____,              
 /    ''---|    //'             
/     \    \ ‾‾ ~               
|  \   \    \
   [/bold white]               
    """
    
    footer = f"""
	""".strip()
    
    combined_text = f"{colored_ascii_art}\n{title}\n{title2}\n{second_ascii_art}\n{footer}"
    console.print(combined_text)

def get_date_range(days):
    end_date = datetime.today()
    start_date = end_date - timedelta(days=days)
    return f"{start_date.strftime('%Y-%m-%d')}..{end_date.strftime('%Y-%m-%d')}"

def run_leak_scanner():
    console.print("[bold magenta]\n🔎 Scanning database leaks...\n[/bold magenta]")
    days = Prompt.ask("[bold yellow]Enter number of days for the search [/bold yellow]", default=str(DEFAULT_DAYS))
    query = Prompt.ask("[bold yellow]Enter query (leave empty for all leaks)[/bold yellow]", default="")
    
    if query.strip():
        script_path = "modules/scrapper_leak_querry.py"
        args = ["-d", str(days), "-q"] + query.split()
    else:
        script_path = "modules/scrapper_leak_normal.py"
        args = ["-d", str(days)]
    
    if not os.path.exists(script_path):
        console.print(f"[bold red]❌ Error: {script_path} not found![/bold red]")
        return
    
    try:
        result = subprocess.run(["python3", script_path] + args, capture_output=True, text=True, check=True)
        console.print(f"[bold green]✅ Leak Scan Results:[/bold green]\n{result.stdout}")
    except subprocess.CalledProcessError as e:
        console.print(f"[bold red]❌ Leak scanner error: {e.stderr}[/bold red]")
    
    Prompt.ask("[bold cyan]Press Enter to return to the menu...[/bold cyan]", default="")

    os.system('clear' if os.name == 'posix' else 'cls')
    
    menu_selection()

def run_cve_scanner():
    console.print("[bold magenta]\n🛡️ Scanning CVE Advisories...\n[/bold magenta]")
    severity = Prompt.ask("[bold yellow]Enter severity level (default: critical)[/bold yellow]", default="critical")
    days = Prompt.ask("[bold yellow]Enter number of days for the search (-d value)[/bold yellow]", default=str(DEFAULT_DAYS))
    query = Prompt.ask("[bold yellow]Enter query (leave empty for all advisories)[/bold yellow]", default="")

    script_path = "modules/CVE_Advisories_Parser.py"
    
    if not os.path.exists(script_path):
        console.print(f"[bold red]❌ Error: {script_path} not found![/bold red]")
        return
    
    args = ["-s", severity, "-d", str(days)]
    if query.strip():
        args.extend(["-q", query])

    try:
        result = subprocess.run(["python3", script_path] + args, capture_output=True, text=True, check=True)
        console.print(f"[bold green]✅ CVE Scan Results:[/bold green]\n{result.stdout}")
    except subprocess.CalledProcessError as e:
        console.print(f"[bold red]❌ CVE scanner error: {e.stderr}[/bold red]")

    Prompt.ask("[bold cyan]Press Enter to return to the menu...[/bold cyan]", default="")

    os.system('clear' if os.name == 'posix' else 'cls')
    
    menu_selection()

def menu_selection():
    display_derrick()
    console.print("\n[bold cyan]Select an option:[/bold cyan]")
    console.print("[bold yellow][1][/bold yellow] [bold white]Scan database leaks[/bold white]  |  "
                  "[bold yellow][2][/bold yellow] [bold white]Scan CVE Advisories[/bold white]  |  "
                  "[bold red]\[q][/bold red] [bold white]Quit[/bold white]\n")

    while True:
        choice = Prompt.ask("\n[bold yellow]Enter your choice [/bold yellow]", choices=["1", "2", "q"], default="1")
        
        if choice == "1":
            run_leak_scanner()
        elif choice == "2":
            run_cve_scanner()
        elif choice == "q":
            console.print("[bold red]🚪 Exiting program.[/bold red]")
            exit(0)



if __name__ == "__main__":
    try:
        menu_selection()
    except KeyboardInterrupt:
        console.print("\n[bold red]❌ Interrupted by user. Exiting...[/bold red]")
        exit(0)

