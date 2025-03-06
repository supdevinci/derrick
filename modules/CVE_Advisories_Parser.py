import subprocess
import json
import argparse
import os
from datetime import datetime, timedelta
from rich.console import Console

console = Console()

def run_bash_script(severity, query, published):
    """
    Exécute le script Bash avec les arguments spécifiés et récupère la sortie JSON.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))  # Obtient le chemin du dossier modules
    script_path = os.path.join(script_dir, "CVE_Advisories.sh")  # Construit le chemin absolu

    command = [script_path, f"--severity={severity}", f"--published={published}"]
    
    if query:
        command.append(f"--query={query}")
    
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        return None

def parse_json_output(json_str):
    """
    Parse le JSON récupéré et extrait les informations essentielles.
    """
    try:
        advisories = json.loads(json_str)
        if not advisories:
            console.print("[bold red]Aucun résultat trouvé.[/bold red]")
            return
        
        if isinstance(advisories, list) and len(advisories) > 0:
            advisories = advisories[0]  # Suppression du tableau imbriqué inutile
        
        for advisory in advisories:
            ghsa_id = advisory.get("ghsa_id", "N/A")
            cve_id = advisory.get("cve_id", "N/A")
            summary = advisory.get("summary", "N/A")
            url = advisory.get("html_url", advisory.get("url", "N/A"))
            date_published = advisory.get("published_at", "N/A")
            references = advisory.get("references", [])
            cvss_score = advisory.get("cvss", {}).get("score", "N/A")
            
            console.print("\n[bold cyan]CVE:[/bold cyan]", cve_id)
            console.print("[bold cyan]GHSA:[/bold cyan]", ghsa_id)
            console.print("[bold cyan]Résumé:[/bold cyan]", summary)
            console.print("[bold cyan]URL:[/bold cyan]", url)
            console.print("[bold cyan]Date de publication:[/bold cyan]", date_published)
            console.print("[bold cyan]Score CVSS:[/bold cyan]", cvss_score)
            console.print("[bold cyan]Références:[/bold cyan]")
            
            for ref in references:
                console.print(f"    ➜ [blue]{ref}[/blue]")
            
            console.print("-" * 40)
    
    except json.JSONDecodeError:
        console.print("[bold red]Aucun résultat trouvé.[/bold red]")

def calculate_published_date(days):
    """
    Calcule la période de publication basée sur le nombre de jours donné.
    """
    end_date = datetime.today().strftime("%Y-%m-%d")
    start_date = (datetime.today() - timedelta(days=days)).strftime("%Y-%m-%d")
    return f"{start_date}..{end_date}"

def main():
    parser = argparse.ArgumentParser(description="Exécute CVE_Advisories.sh et formate la sortie JSON.")
    parser.add_argument("-s", "--severity", default="critical", help="Niveau de sévérité (par défaut: critical)")
    parser.add_argument("-q", "--query", help="Terme de recherche pour l'advisory (optionnel)")
    parser.add_argument("-d", "--days", type=int, default=5, help="Nombre de jours pour la recherche de publications (par défaut: 5)")
    args = parser.parse_args()
    
    published_range = calculate_published_date(args.days)
    json_output = run_bash_script(args.severity, args.query, published_range)
    
    if json_output:
        parse_json_output(json_output)

if __name__ == "__main__":
    main()
