from rich.text import Text
from rich.style import Style
from rich.live import Live
import time
import random
import requests
import shutil
import argparse
from bs4 import BeautifulSoup
from rich.console import Console
from rich.progress import Progress, BarColumn, TextColumn, TimeElapsedColumn

# Initialize Rich for styling and color
console = Console()



# Argument to change the datecut value
def parse_arguments():
    parser = argparse.ArgumentParser(description="Scraper BreachForums")
    parser.add_argument("-d", "--datecut", type=int, default=5, help="Change the datecut value (default 5)")
    return parser.parse_args()

args = parse_arguments()
datecut_value = args.datecut

# Base URL
base_url = "https://breachforums.st"

# Load cookies from a cookies.txt file
cookies = {}
try:
    with open('cookies.txt', 'r') as file:
        for line in file:
            if not line.startswith('#') and line.strip() != '':
                try:
                    parts = line.strip().split('\t')
                    if len(parts) == 7:
                        domain, flag, path, secure, expiration, name, value = parts
                        cookies[name] = value
                except ValueError:
                    pass
except FileNotFoundError:
    console.print("[bold red]Error: cookies.txt file not found![/bold red]")
    exit(1)

# User-Agent header
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

def get_total_pages(soup):
    pagination = soup.find(class_="pagination")
    if pagination:
        page_links = pagination.find_all('a', href=True)
        page_numbers = [int(link['href'].split('page=')[1].split('&')[0]) for link in page_links if 'page=' in link['href']]
        return max(page_numbers) if page_numbers else 1
    return 1

def scrape_page(url):
    response = requests.get(url, headers=headers, cookies=cookies)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        subjects = soup.find_all(class_="subject_new")
        results = []
        
        for subject in subjects:
            subject_text = subject.get_text(strip=True)
            subject_url = subject.find('a')['href']
            full_url = f"{base_url}/{subject_url}"
            
            # Trouver la date du sujet
            date_tag = subject.find_next(class_="forum-display__thread-date")
            date = date_tag.get_text(strip=True) if date_tag else "Date non trouvée"
            
            results.append((subject_text, full_url, date))
        
        return results
    return []

def run_scraper():
    console.print("[bold magenta]Starting scanning...[/bold magenta]")
    first_page_url = f"{base_url}/Forum-Databases?page=1&datecut={datecut_value}&sortby=started&order=desc&prefix=14"
    response = requests.get(first_page_url, headers=headers, cookies=cookies)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        total_pages = get_total_pages(soup)
        console.print(f"[bold cyan]Total pages found: {total_pages}[/bold cyan]")
        
        results = []
        with Progress() as progress:
            task = progress.add_task("[cyan]Scraping...", total=total_pages)
            
            for page in range(1, total_pages + 1):
                page_url = f"{base_url}/Forum-Databases?page={page}&datecut={datecut_value}&sortby=started&order=desc&prefix=14"
                results.extend(scrape_page(page_url))
                progress.update(task, advance=1)
                time.sleep(0.3)
        
        console.print(f"[bold cyan]\nResults found ({len(results)}) :\n\n[/bold cyan]")
        for subject, url, date in results:
            console.print(f"[bold cyan]Leaked:[/bold cyan] {subject}")
            console.print(f"[bold green]URL:[/bold green] {url}")
            console.print(f"[bold yellow]DATE:[/bold yellow] {date}")
            console.print("-" * 40, style="dim")
    else:
        console.print(f"[bold red]Error during request: {response.status_code}[/bold red]")

# Then, run the scraper
run_scraper()

