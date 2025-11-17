#!/usr/bin/env python3
import os
import requests
from collections import Counter
import base64

def get_github_languages():
    """Get languages from all repositories using GitHub API"""
    token = os.getenv('GITHUB_TOKEN')
    username = "Moin-Sikder"  # Replace with your username
    
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    # Get all repositories
    repos_url = f"https://api.github.com/users/{username}/repos?per_page=100"
    response = requests.get(repos_url, headers=headers)
    repos = response.json()
    
    all_languages = Counter()
    
    for repo in repos:
        if not repo['fork']:  # Skip forks
            langs_url = repo['languages_url']
            langs_response = requests.get(langs_url, headers=headers)
            if langs_response.status_code == 200:
                repo_langs = langs_response.json()
                for lang, bytes_count in repo_langs.items():
                    all_languages[lang] += 1
    
    return dict(all_languages)

def create_badge_url(language, count):
    """Create custom badge for each language"""
    color_map = {
        'Python': '3776AB',
        'JavaScript': 'F7DF1E',
        'TypeScript': '3178C6',
        'R': '276DC3',
        'Shell': '4EAA25',
        'HTML': 'E34F26',
        'CSS': '1572B6',
        'Dockerfile': '2496ED',
        'Jupyter Notebook': 'DA5B0B'
    }
    
    color = color_map.get(language, '6f42c1')
    return f"https://img.shields.io/badge/{language}-{count}-{color}?style=flat-square"

def update_readme_advanced(language_data):
    readme_path = 'README.md'
    
    with open(readme_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Create advanced dashboard
    dashboard = """## 📊 Automated Project Dashboard

<div align="center">

### 🛠️ Language Distribution Across All Repositories

"""
    
    # Add badges
    for lang, count in sorted(language_data.items(), key=lambda x: x[1], reverse=True):
        badge_url = create_badge_url(lang, count)
        dashboard += f"![{lang}]({badge_url}) "
    
    dashboard += """

### 📈 Detailed Breakdown

| Language | Repository Count | Percentage |
|----------|-----------------|------------|
"""
    
    total_repos = sum(language_data.values())
    
    for lang, count in sorted(language_data.items(), key=lambda x: x[1], reverse=True):
        percentage = (count / total_repos) * 100 if total_repos > 0 else 0
        dashboard += f"| `{lang}` | {count} | {percentage:.1f}% |\n"
    
    dashboard += f"""
**Total Languages:** {len(language_data)} | **Total Repositories Analyzed:** {total_repos}

*Last updated automatically via GitHub Actions*

</div>

---
"""
    
    # Update README
    if '## 📊 Automated Project Dashboard' in content:
        start = content.find('## 📊 Automated Project Dashboard')
        end = content.find('---', start) + 3
        content = content[:start] + dashboard + content[end:]
    else:
        # Find where to insert (after welcome section)
        welcome_end = content.find('---', content.find('---') + 3) + 3
        content = content[:welcome_end] + '\n' + dashboard + content[welcome_end:]
    
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(content)

if __name__ == "__main__":
    # Try GitHub API first, fall back to file detection
    try:
        languages = get_github_languages()
        print("Using GitHub API data")
    except:
        from update_languages import detect_languages
        languages = detect_languages()
        print("Using file detection data")
    
    print("Language data:", languages)
    update_readme_advanced(languages)