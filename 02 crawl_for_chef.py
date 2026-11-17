import sqlite3
import json
import requests
from bs4 import BeautifulSoup
from typing import Optional

DB_NAME = "recipes_base.db"

def extract_chef_from_url(url: str) -> Optional[str]:
    """Crawls a source_url locally to extract author/chef meta tags or schema JSON-LD."""
    if not url or not url.startswith("http"):
        return None
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Compatible; RecipeBot/1.0)"}
        resp = requests.get(url, headers=headers, timeout=5)
        if resp.status_code != 200:
            return None
            
        soup = BeautifulSoup(resp.text, "html.parser")
        
        # 1. Check common author meta tags
        meta_author = soup.find("meta", attrs={"name": ["author", "article:author", "og:article:author"]})
        if meta_author and meta_author.get("content"):
            return meta_author["content"].strip()
            
        # 2. Check schema.org author JSON-LD or microdata
        for script in soup.find_all("script", type="application/ld+json"):
            try:
                data = json.loads(script.string or "")
                if isinstance(data, dict):
                    author = data.get("author")
                    if isinstance(author, dict) and author.get("name"):
                        return author["name"].strip()
                    elif isinstance(author, str):
                        return author.strip()
                elif isinstance(data, list):
                    for item in data:
                        if isinstance(item, dict) and "author" in item:
                            auth = item["author"]
                            if isinstance(auth, dict) and auth.get("name"):
                                return auth["name"].strip()
                            elif isinstance(auth, str):
                                return auth.strip()
            except Exception:
                continue
                
        return None
    except Exception:
        return None

def crawl_and_update_chefs(db_path: str = DB_NAME):
    """Scans the SQLite database for records with source_url and empty chef, then crawls and updates."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Fetch recipes that have a source_url but no chef yet
    cursor.execute("SELECT recipe_id, source_url FROM recipes WHERE source_url IS NOT NULL AND (chef IS NULL OR chef = '')")
    rows = cursor.fetchall()
    
    print(f"Found {len(rows)} recipes with source URLs to crawl for chef metadata.")
    
    updated_count = 0
    for recipe_id, source_url in rows:
        print(f"Crawling: {source_url} ...", end=" ")
        chef_name = extract_chef_from_url(source_url)
        if chef_name:
            cursor.execute("UPDATE recipes SET chef = ? WHERE recipe_id = ?", (chef_name, recipe_id))
            print(f"Found chef: {chef_name}")
            updated_count += 1
        else:
            print("No chef found.")
            
    conn.commit()
    conn.close()
    print(f"Finished. Updated {updated_count} records with chef metadata.")

if __name__ == "__main__":
    crawl_and_update_chefs()