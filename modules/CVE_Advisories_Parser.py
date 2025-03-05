import subprocess
import json
import argparse
import os
from datetime import datetime, timedelta

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
            return "\033[1;31mAucun résultat trouvé.\033[0m"
        
        if isinstance(advisories, list) and len(advisories) > 0:
            advisories = advisories[0]  # Suppression du tableau imbriqué inutile
        
        output = []
        for advisory in advisories:
            ghsa_id = advisory.get("ghsa_id", "N/A")
            cve_id = advisory.get("cve_id", "N/A")
            summary = advisory.get("summary", "N/A")
            url = advisory.get("html_url", advisory.get("url", "N/A"))
            date_published = advisory.get("published_at", "N/A")
            references = advisory.get("references", [])
            cvss_score = advisory.get("cvss", {}).get("score", "N/A")
            
            references_str = "\n           ➜ ".join(references) if references else "Aucune référence disponible"
            
            formatted_entry = f"""
\033[1;36mCVE:\033[0m {cve_id}
\033[1;36mGHSA:\033[0m {ghsa_id}
\033[1;36mRésumé:\033[0m {summary}
\033[1;36mURL:\033[0m {url}
\033[1;36mDate de publication:\033[0m {date_published}
\033[1;36mScore CVSS:\033[0m {cvss_score}
\033[1;36mRéférences:\033[0m
           ➜ {references_str}
----------------------------------------
""".strip()
            output.append(formatted_entry)
        
        return "\n".join(output)
    except json.JSONDecodeError:
        return "\033[1;31mAucun résultat trouvé.\033[0m"

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
        formatted_output = parse_json_output(json_output)
        print(formatted_output)

if __name__ == "__main__":
    main()

