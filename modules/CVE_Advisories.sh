#!/bin/bash

# Script to interact with the GitHub Security Advisories API
# Replace <YOUR-TOKEN> with your GitHub authentication token

GITHUB_TOKEN="xxx_XXXXXXXXXXXXX"
BASE_URL="https://api.github.com/advisories"

# Function to display usage instructions
usage() {
  echo "Usage: $0 [OPTIONS]"
  echo "Options:"
  echo "  --query=<keyword>               Filter advisories containing a specific keyword (e.g., Fortinet, VMware)"
  echo "  --ghsa_id=<GHSA-ID>             Filter by GHSA-ID"
  echo "  --type=<type>                   Filter by type (reviewed, malware, unreviewed)"
  echo "  --cve_id=<CVE-ID>               Filter by CVE-ID"
  echo "  --ecosystem=<ecosystem>         Filter by ecosystem (npm, pip, etc.)"
  echo "  --severity=<severity>           Filter by severity (low, medium, high, critical)"
  echo "  --cwes=<cwe-list>               Filter by CWEs (example: 79,284)"
  echo "  --is_withdrawn=<true|false>     Include only withdrawn advisories"
  echo "  --affects=<package-list>        Filter by affected packages"
  echo "  --published=<date-range>        Filter by publication date (e.g., 2023-01-01..2023-12-31)"
  echo "  --updated=<date-range>          Filter by update date"
  echo "  --modified=<date-range>         Filter by modification date"
  echo "  --epss_percentage=<value>       Filter by EPSS percentage"
  echo "  --epss_percentile=<value>       Filter by EPSS percentile"
  echo "  --direction=<asc|desc>          Sort order (default: desc)"
  echo "  --sort=<property>               Property to sort by (published, updated, etc.)"
  echo "  --last=<N>                      Show only the last N results (default: 10)"
  echo "  --add-token=<GITHUB_TOKEN>      Add or update the GitHub token"
}

# Initialize parameters
PARAMS="direction=desc&per_page=100"
QUERY_KEYWORD=""
LAST_COUNT=10 # Default to 10 results if --last is not provided
RESULTS_COUNT=0 # Counter for the number of matching results
COLLECTED_RESULTS="[]" # Initialize empty JSON array for results

# Parse arguments
for arg in "$@"; do
  case $arg in
    --query=*)
      QUERY_KEYWORD="${arg#*=}"
      ;;
    --ghsa_id=*)
      ghsa_id="${arg#*=}"
      PARAMS+="&ghsa_id=$ghsa_id"
      ;;
    --type=*)
      type="${arg#*=}"
      PARAMS+="&type=$type"
      ;;
    --cve_id=*)
      cve_id="${arg#*=}"
      PARAMS+="&cve_id=$cve_id"
      ;;
    --ecosystem=*)
      ecosystem="${arg#*=}"
      PARAMS+="&ecosystem=$ecosystem"
      ;;
    --severity=*)
      severity="${arg#*=}"
      PARAMS+="&severity=$severity"
      ;;
    --cwes=*)
      cwes="${arg#*=}"
      PARAMS+="&cwes=$cwes"
      ;;
    --is_withdrawn=*)
      is_withdrawn="${arg#*=}"
      PARAMS+="&is_withdrawn=$is_withdrawn"
      ;;
    --affects=*)
      affects="${arg#*=}"
      PARAMS+="&affects=$affects"
      ;;
    --published=*)
      published="${arg#*=}"
      PARAMS+="&published=$published"
      ;;
    --updated=*)
      updated="${arg#*=}"
      PARAMS+="&updated=$updated"
      ;;
    --modified=*)
      modified="${arg#*=}"
      PARAMS+="&modified=$modified"
      ;;
    --epss_percentage=*)
      epss_percentage="${arg#*=}"
      PARAMS+="&epss_percentage=$epss_percentage"
      ;;
    --epss_percentile=*)
      epss_percentile="${arg#*=}"
      PARAMS+="&epss_percentile=$epss_percentile"
      ;;
    --direction=*)
      direction="${arg#*=}"
      PARAMS="${PARAMS//direction=desc/}&direction=$direction"
      ;;
    --sort=*)
      sort="${arg#*=}"
      PARAMS+="&sort=$sort"
      ;;
    --last=*)
      LAST_COUNT="${arg#*=}"
      ;;
    --add-token=*)
      new_token="${arg#*=}"
      escaped_token=$(printf '%s\n' "$new_token" | sed 's/[\/&]/\\&/g')
      sed -i "s/^GITHUB_TOKEN=.*/GITHUB_TOKEN=\"$escaped_token\"/" "$0"
      echo "GitHub token successfully updated."
      exit 0
      ;;
    *)
      echo "Unknown option: $arg"
      usage
      exit 1
      ;;
  esac
done

# Function to fetch advisories
fetch_advisories() {
  local url="$1"
  curl -i -s -L \
    -H "Accept: application/vnd.github+json" \
    -H "Authorization: Bearer $GITHUB_TOKEN" \
    -H "X-GitHub-Api-Version: 2022-11-28" \
    "$url"
}

# Start URL
URL="$BASE_URL?$PARAMS"
NEXT_URL="$URL"

# Fetch pages until the desired number of results is found
while [ -n "$NEXT_URL" ] && [ "$RESULTS_COUNT" -lt "$LAST_COUNT" ]; do
  response=$(fetch_advisories "$NEXT_URL")

  # Extract the headers and body
  headers=$(echo "$response" | sed -n '/^HTTP\/2 200/,/^$/p')
  body=$(echo "$response" | sed -n '/^\[/,$p')

  # Check if the response is valid JSON
  if echo "$body" | jq -e . > /dev/null 2>&1; then
    # Filter results by keyword if specified
    if [ -n "$QUERY_KEYWORD" ]; then
      matching_results=$(echo "$body" | jq --arg keyword "$QUERY_KEYWORD" '
        .[] | select(
          (.summary | test($keyword; "i")) or
          (.description | test($keyword; "i"))
        )'
      )
    else
      matching_results=$(echo "$body")
    fi

    # Add matching results to the collected results
    if [ -n "$matching_results" ]; then
      COLLECTED_RESULTS=$(echo "$COLLECTED_RESULTS" "$matching_results" | jq -s 'flatten')
      RESULTS_COUNT=$(echo "$COLLECTED_RESULTS" | jq 'length')
    fi

    # Stop if the desired number of results is reached
    if [ "$RESULTS_COUNT" -ge "$LAST_COUNT" ]; then
      break
    fi
  fi

  # Check if there is a next page
  if echo "$headers" | grep -q 'rel="next"'; then
	NEXT_URL=$(echo "$headers" | grep -Eo '<[^>]+>; rel="next"' | sed -E 's/^<([^>]+)>; rel="next"/\1/')
  else
    NEXT_URL=""
  fi
done

# Display the results
if [ "$RESULTS_COUNT" -eq 0 ]; then
  echo "No results found."
else
  echo "$COLLECTED_RESULTS" | jq -s ".[0:$LAST_COUNT]"
fi
