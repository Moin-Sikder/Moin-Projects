import requests
from bs4 import BeautifulSoup
import urllib.parse
import pandas as pd
import time
import random

def search_google_images(query, num_results=10):
    """
    Search for meme images using Google Images
    """
    print(f"🔍 Searching Google Images for '{query}' memes...")
    
    meme_links = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    try:
        # Search query for memes
        search_query = f"{query} memes"
        encoded_query = urllib.parse.quote_plus(search_query)
        url = f"https://www.google.com/search?q={encoded_query}&tbm=isch"
        
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find image elements
        images = soup.find_all('img')
        
        for i, img in enumerate(images[1:num_results+1]):  # Skip first logo
            img_src = img.get('src')
            if img_src and img_src.startswith('http'):
                meme_links.append({
                    'title': f"{query} meme {i+1}",
                    'url': img_src,
                    'source': 'Google Images',
                    'type': 'image'
                })
                
    except Exception as e:
        print(f"Error searching Google Images: {e}")
    
    return meme_links

def search_reddit_memes_simple(query, num_results=10):
    """
    Search for memes using Reddit search (without API)
    """
    print(f"🔍 Searching Reddit for '{query}' memes...")
    
    meme_links = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        search_query = urllib.parse.quote_plus(query)
        url = f"https://www.reddit.com/search/?q={search_query}&type=link"
        
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Look for post links
        posts = soup.find_all('a', href=True)
        
        for post in posts[:num_results]:
            href = post.get('href', '')
            if '/r/' in href and '/comments/' in href:
                full_url = f"https://reddit.com{href}" if href.startswith('/') else href
                meme_links.append({
                    'title': post.get_text(strip=True) or f"Reddit meme about {query}",
                    'url': full_url,
                    'source': 'Reddit',
                    'type': 'post'
                })
                
    except Exception as e:
        print(f"Error searching Reddit: {e}")
    
    return meme_links

def search_meme_websites(query, num_results=5):
    """
    Search popular meme websites
    """
    print(f"🔍 Searching meme websites for '{query}'...")
    
    meme_links = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    # List of meme website search URLs
    meme_sites = [
        f"https://imgflip.com/memesearch?q={urllib.parse.quote_plus(query)}",
        f"https://knowyourmeme.com/search?q={urllib.parse.quote_plus(query)}"
    ]
    
    for site_url in meme_sites:
        try:
            response = requests.get(site_url, headers=headers)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Look for images and links
            images = soup.find_all('img', src=True)
            
            for img in images[:num_results]:
                src = img.get('src')
                if src and any(ext in src.lower() for ext in ['.jpg', '.jpeg', '.png', '.gif']):
                    full_url = src if src.startswith('http') else urllib.parse.urljoin(site_url, src)
                    meme_links.append({
                        'title': f"{query} meme from {site_url.split('//')[1].split('/')[0]}",
                        'url': full_url,
                        'source': 'Meme Website',
                        'type': 'image'
                    })
                    
        except Exception as e:
            print(f"Error searching {site_url}: {e}")
    
    return meme_links

def search_bing_images(query, num_results=10):
    """
    Search for memes using Bing Images
    """
    print(f"🔍 Searching Bing Images for '{query}' memes...")
    
    meme_links = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    try:
        search_query = urllib.parse.quote_plus(f"{query} memes")
        url = f"https://www.bing.com/images/search?q={search_query}"
        
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find image elements
        images = soup.find_all('img', {'src': True})
        
        for i, img in enumerate(images[:num_results]):
            src = img.get('src')
            if src and src.startswith('http') and not src.endswith('.svg'):
                meme_links.append({
                    'title': f"{query} meme {i+1}",
                    'url': src,
                    'source': 'Bing Images',
                    'type': 'image'
                })
                
    except Exception as e:
        print(f"Error searching Bing Images: {e}")
    
    return meme_links

def display_results(meme_links):
    """
    Display the found meme links in a nice format
    """
    if not meme_links:
        print("😞 No memes found for your search. Try a different keyword!")
        return
    
    print(f"\n🎉 Found {len(meme_links)} meme links!")
    print("=" * 80)
    
    # Create DataFrame for nice display
    df = pd.DataFrame(meme_links)
    
    # Display in a clean format
    for idx, meme in enumerate(meme_links, 1):
        print(f"\n{idx}. {meme['title']}")
        print(f"   Source: {meme['source']}")
        print(f"   Type: {meme['type']}")
        print(f"   URL: {meme['url']}")
    
    return df

def main():
    """
    Main function to run the Meme Engine
    """
    print("🚀 Welcome to your Personal Meme Engine! 🚀")
    print("=" * 50)
    print("This tool will search for memes across multiple sources...")
    print("No API keys required! Just enter what you're looking for.\n")
    
    # Get user input
    search_query = input("What kind of memes are you looking for?\n👉 Enter your meme description or keywords: ").strip()
    
    if not search_query:
        print("Please enter some keywords to search for memes!")
        return
    
    print(f"\n🕵️ Searching for '{search_query}' memes across the internet...")
    print("This may take a few seconds...\n")
    
    # Search from multiple sources
    all_meme_links = []
    
    # Search Google Images
    all_meme_links.extend(search_google_images(search_query, 8))
    time.sleep(1)  # Be polite to servers
    
    # Search Bing Images
    all_meme_links.extend(search_bing_images(search_query, 8))
    time.sleep(1)
    
    # Search Reddit
    all_meme_links.extend(search_reddit_memes_simple(search_query, 6))
    time.sleep(1)
    
    # Search meme websites
    all_meme_links.extend(search_meme_websites(search_query, 4))
    
    # Remove duplicates
    unique_links = []
    seen_urls = set()
    
    for meme in all_meme_links:
        if meme['url'] not in seen_urls:
            seen_urls.add(meme['url'])
            unique_links.append(meme)
    
    # Display results
    df = display_results(unique_links)
    
    # Save to CSV option
    if unique_links:
        save_csv = input(f"\n💾 Would you like to save these {len(unique_links)} links to a CSV file? (y/n): ").strip().lower()
        if save_csv == 'y':
            filename = f"memes_{search_query.replace(' ', '_')}.csv"
            df.to_csv(filename, index=False)
            print(f"✅ Links saved to '{filename}'")
    
    print(f"\n✨ Search complete! Enjoy your {search_query} memes! ✨")

# Install required packages first
def install_packages():
    """
    Install required packages for Google Colab
    """
    try:
        import requests
        from bs4 import BeautifulSoup
        import pandas as pd
    except ImportError:
        print("📦 Installing required packages...")
        import subprocess
        import sys
        subprocess.check_call([sys.executable, "-m", "pip", "install", "requests", "beautifulsoup4", "pandas", "lxml"])
        print("✅ Packages installed successfully!")

# Run the installation first
install_packages()

# Run the main function
if __name__ == "__main__":
    main()
