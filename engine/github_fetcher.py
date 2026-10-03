"""
Lightweight Public GitHub Scraper & Profile Fetcher for BroCheck
"""

import requests
from typing import Dict, Any

class GitHubFetcher:
    @staticmethod
    def fetch_profile(username: str) -> Dict[str, Any]:
        clean_user = username.strip().lstrip("@").split("/")[-1]
        headers = {
            "User-Agent": "BroCheck-OpenSource-AI/1.0",
            "Accept": "application/vnd.github.v3+json"
        }
        
        try:
            user_url = f"https://api.github.com/users/{clean_user}"
            user_resp = requests.get(user_url, headers=headers, timeout=6)
            
            if user_resp.status_code == 404:
                return {
                    "success": False,
                    "error": f"GitHub user '{clean_user}' does not exist."
                }
            if user_resp.status_code != 200:
                return {
                    "success": False,
                    "error": f"GitHub API error ({user_resp.status_code})."
                }
                
            user_data = user_resp.json()
            
            repos_url = f"https://api.github.com/users/{clean_user}/repos?sort=updated&per_page=10"
            repos_resp = requests.get(repos_url, headers=headers, timeout=6)
            repos_data = repos_resp.json() if repos_resp.status_code == 200 else []
            
            repo_summaries = []
            total_stars = 0
            for r in repos_data:
                stars = r.get("stargazers_count", 0)
                total_stars += stars
                repo_summaries.append(
                    f"- {r.get('name')}: {r.get('description') or 'No description'} "
                    f"(Lang: {r.get('language') or 'None'}, Stars: {stars}, Fork: {r.get('fork')})"
                )
                
            summary_text = (
                f"GitHub User: @{clean_user}\n"
                f"Name: {user_data.get('name') or 'N/A'}\n"
                f"Bio: {user_data.get('bio') or 'No bio (Mysterious or Lazy?)'}\n"
                f"Company: {user_data.get('company') or 'Unemployed / Freelance'}\n"
                f"Public Repos: {user_data.get('public_repos', 0)}\n"
                f"Followers: {user_data.get('followers', 0)} | Following: {user_data.get('following', 0)}\n"
                f"Total Stars on Recent Repos: {total_stars}\n"
                f"Recent Repositories:\n" + ("\n".join(repo_summaries) if repo_summaries else "No public repositories found.")
            )
            
            return {
                "success": True,
                "username": clean_user,
                "summary": summary_text,
                "raw": user_data
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to connect to GitHub: {str(e)}"
            }
