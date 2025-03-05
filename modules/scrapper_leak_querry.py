import requests
from bs4 import BeautifulSoup
from rich.console import Console
import argparse

# Initialisation de la console
console = Console()

# Base URL de BreachForums
BASE_URL = "https://breachforums.st"

# Chargement des cookies depuis le fichier cookies.txt
def load_cookies():
    cookies = {}
    try:
        with open("cookies.txt", "r") as file:
            for line in file:
                if not line.startswith("#") and line.strip():
                    parts = line.strip().split("\t")
                    if len(parts) == 7:
                        domain, flag, path, secure, expiration, name, value = parts
                        cookies[name] = value
    except FileNotFoundError:
        console.print("[bold red]Error: cookies.txt not found![/bold red]")
        exit(1)
    return cookies

# Headers pour éviter d’être bloqué
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# Arguments pour la datecut et la recherche
def parse_arguments():
    parser = argparse.ArgumentParser(description="Scraper BreachForums")
    parser.add_argument("-d", "--datecut", type=int, default=7, help="Nombre de jours pour la recherche (par défaut 7)")
    parser.add_argument("-q", "--query", nargs="+", help="Mots-clés de recherche (ex: -q france vpn leak)")
    return parser.parse_args()

args = parse_arguments()
DATECUT_VALUE = args.datecut
QUERY_LIST = args.query if args.query else []

# Construire l'URL avec les filtres
def build_url():
    if QUERY_LIST:
        # Recherche avancée avec query
        keywords_str = "+".join(QUERY_LIST)
        return f"{BASE_URL}/search.php?action=do_search&keywords={keywords_str}&postthread=2&author=&matchusername=1&forums[]=all&findthreadst=1&numreplies=&postdate={DATECUT_VALUE}&pddir=1&threadprefix[]=14&sortby=lastpost&sortordr=desc&showresults=threads&submit=Search"
    else:
        # Recherche standard dans les bases de données leaks
        return f"{BASE_URL}/Forum-Databases?datecut={DATECUT_VALUE}&sortby=started&order=desc&prefix=14"

# Scraper une page spécifique
def scrape_page():
    url = build_url()
    response = requests.get(url, headers=HEADERS, cookies=load_cookies())

    if response.status_code != 200:
        console.print(f"[bold red]Error fetching page: {response.status_code}[/bold red]")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    
    # Vérification si on est sur la bonne page de résultats
    if QUERY_LIST:
        results_table = soup.find("table", class_="tborder")
        if not results_table:
            console.print("[bold red]No results found for your query.[/bold red]")
            return []
        subjects = results_table.find_all("a", class_="subject_new")
    else:
        subjects = soup.find_all(class_="subject_new")

    leaks = []
    for subject in subjects:
        title = subject.get_text(strip=True)
        link = subject.get("href")

        if not link:
            continue  # Skip si aucun lien trouvé

        full_url = f"{BASE_URL}/{link}"

        # Trouver la date (spécifique aux threads)
        date_tag = subject.find_parent("tr").find_all("td")[-1]
        date = date_tag.get_text(strip=True) if date_tag else "Unknown Date"

        leaks.append({"title": title, "url": full_url, "date": date})

    return leaks

# Fonction principale pour scraper les résultats
def run_scraper():
    console.print("[bold yellow]Scanning database leaks...[/bold yellow]")

    leaks = scrape_page()

    # Affichage des résultats
    if not leaks:
        console.print("[bold red]No leaks found.[/bold red]")
        return

    console.print(f"\n[bold cyan]Leaks found ({len(leaks)}):\n[/bold cyan]")

    for leak in leaks:
        console.print(f"[bold cyan]Leak:[/bold cyan] {leak['title']}")
        console.print(f"[bold green]URL:[/bold green] {leak['url']}")
        console.print(f"[bold yellow]Date:[/bold yellow] {leak['date']}")
        console.print("-" * 60)

# Exécution du scraper
if __name__ == "__main__":
    run_scraper()

