import hashlib
import json
import os
import re
import sqlite3
from typing import Dict, List, Optional
import requests
from bs4 import BeautifulSoup

DB_NAME = "recipes_base.db"

CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS "recipes" (
    recipe_id TEXT PRIMARY KEY,
    source_content_hash TEXT NOT NULL,
    title TEXT NOT NULL,
    dish_type TEXT NOT NULL CHECK(dish_type IN ('main', 'side')),
    dish_subtype TEXT CHECK(dish_subtype IN (
        'vegetable', 
        'starch', 
        'rice', 
        'grain', 
        'salad', 
        'bread', 
        'soup', 
        'pasta', 
        'stir-fry', 
        'appetizer', 
        'stew', 
        'dessert'
    )),
    cuisine TEXT,
    vibe_json TEXT,
    season_json TEXT,
    dietary_flags_json TEXT,
    active_prep_time_minutes INTEGER,
    marinade_time TEXT,
    cook_time_minutes INTEGER,
    cook_time_attention_minutes INTEGER,
    oven_time_minutes INTEGER,
    effort_level TEXT NOT NULL CHECK(effort_level IN ('Low', 'Medium', 'Medium-High', 'High')),
    effort_rationale TEXT,
    equipment_needed_json TEXT,
    ingredient_master_list_json TEXT,
    historical_pairing_ids_json TEXT,
    source_url TEXT,
    chef TEXT,
    blueprint_markdown TEXT NOT NULL,
    embedding BLOB NOT NULL
);
"""

def init_db(db_path: str = DB_NAME):
    """Initializes SQLite database with the updated PRD schema."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(CREATE_TABLE_SQL)
    conn.commit()
    conn.close()
    print(f"Database initialized: {db_path}")

def extract_chef_from_url(url: Optional[str]) -> Optional[str]:
    """Crawls source_url locally to extract author/chef meta tags or bylines."""
    if not url or not url.startswith("http"):
        return None
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Compatible; RecipeBot/1.0)"}
        resp = requests.get(url, headers=headers, timeout=5)
        if resp.status_code != 200:
            return None
            
        soup = BeautifulSoup(resp.text, "html.parser")
        
        # Check common author meta tags
        meta_author = soup.find("meta", attrs={"name": ["author", "article:author", "og:article:author"]})
        if meta_author and meta_author.get("content"):
            return meta_author["content"].strip()
            
        # Check schema.org author JSON-LD or microdata
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
            except Exception:
                continue
                
        return None
    except Exception:
        # Fail gracefully on network errors or timeouts during offline build
        return None

def parse_cleaned_markdown(file_path: str) -> List[Dict]:
    """
    Parses a cleaned markdown file, segments mains and nested side dishes,
    computes hashes, extracts URLs, and infers seasonal context.
    """
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return []
        
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    lines = content.splitlines()
    parsed_recipes = []
    
    current_month_year = None
    current_main = None
    current_header = None
    current_lines = []
    
    def flush_recipe(header: str, lines_list: List[str], is_side: bool = False, parent_title: Optional[str] = None):
        if not header or not lines_list:
            return
            
        header_clean = re.sub(r"\s*\{#.*?\}\s*$", "", header.strip())
        link_match = re.match(r"^(#{1,6})\s+\[(.*?)\]\((.*?)\)$", header_clean)
        
        if link_match:
            title = link_match.group(2).strip()
            source_url = link_match.group(3).strip()
        else:
            title_match = re.match(r"^#{1,6}\s+(.*)$", header_clean)
            title = title_match.group(1).strip() if title_match else header_clean
            source_url = None
            
        if re.match(r"^(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4}$", title, re.IGNORECASE):
            return
            
        block_text = "\n".join(lines_list).strip()
        if not block_text:
            return
            
        content_hash = hashlib.sha256(block_text.encode("utf-8")).hexdigest()
        slug = re.sub(r"[^a-z0-9]+", "_", title.lower()).strip("_")
        recipe_id = f"rec_{slug[:30]}_{content_hash[:6]}"
        
        # Seasonal inference from active month context
        season_list = []
        if current_month_year:
            m_lower = current_month_year.lower()
            if any(m in m_lower for m in ["december", "january", "february"]):
                season_list.append("winter")
            if any(m in m_lower for m in ["march", "april", "may"]):
                season_list.append("spring")
            if any(m in m_lower for m in ["june", "july", "august"]):
                season_list.append("summer")
            if any(m in m_lower for m in ["september", "october", "november"]):
                season_list.append("autumn")
                
        dish_type = "side" if is_side else "main"
        
        parsed_recipes.append({
            "recipe_id": recipe_id,
            "source_content_hash": content_hash,
            "title": title,
            "dish_type": dish_type,
            "dish_subtype": None,
            "cuisine": None,
            "vibe_json": None,
            "season_json": json.dumps(season_list) if season_list else None,
            "dietary_flags_json": None,
            "active_prep_time_minutes": None,
            "marinade_time": None,
            "cook_time_minutes": None,
            "cook_time_attention_minutes": None,
            "oven_time_minutes": None,
            "effort_level": "Medium",
            "effort_rationale": None,
            "equipment_needed_json": None,
            "ingredient_master_list_json": None,
            "historical_pairing_ids_json": json.dumps([parent_title]) if parent_title else None,
            "source_url": source_url,
            "chef": None,
            "blueprint_markdown": block_text,
            "embedding": b""
        })

    # State machine parsing through lines
    for line in lines:
        stripped = line.strip()
        
        # Track Month/Year context headers
        month_match = re.match(r"^#+\s+((?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4})", stripped, re.IGNORECASE)
        if month_match:
            if current_header:
                flush_recipe(current_header, current_lines)
            current_month_year = month_match.group(1)
            current_header = None
            current_lines = []
            current_main = None
            continue
            
        # Detect headers (# to ####)
        header_match = re.match(r"^(#{1,4})\s+(.*)$", line)
        if header_match:
            hashes, title_text = header_match.groups()
            level = len(hashes)
            
            if current_header:
                # Flush previous block
                is_side_flag = (current_main is not None and level > 2)
                parent = current_main if is_side_flag else None
                flush_recipe(current_header, current_lines, is_side=is_side_flag, parent_title=parent)
                
            current_header = line
            current_lines = [line]
            
            if level <= 2:
                current_main = title_text.strip()
        else:
            if current_header is not None:
                current_lines.append(line)
                
    if current_header:
        flush_recipe(current_header, current_lines)
        
    return parsed_recipes

def load_to_db(recipes: List[Dict], db_path: str = DB_NAME, crawl_chefs: bool = False):
    """Inserts recipes into SQLite, optionally crawling URLs for chef names."""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    insert_sql = """
    INSERT OR REPLACE INTO recipes (
        recipe_id, source_content_hash, title, dish_type, dish_subtype,
        cuisine, vibe_json, season_json, dietary_flags_json,
        active_prep_time_minutes, marinade_time, cook_time_minutes,
        cook_time_attention_minutes, oven_time_minutes, effort_level,
        effort_rationale, equipment_needed_json, ingredient_master_list_json,
        historical_pairing_ids_json, source_url, chef, blueprint_markdown, embedding
    ) VALUES (
        :recipe_id, :source_content_hash, :title, :dish_type, :dish_subtype,
        :cuisine, :vibe_json, :season_json, :dietary_flags_json,
        :active_prep_time_minutes, :marinade_time, :cook_time_minutes,
        :cook_time_attention_minutes, :oven_time_minutes, :effort_level,
        :effort_rationale, :equipment_needed_json, :ingredient_master_list_json,
        :historical_pairing_ids_json, :source_url, :chef, :blueprint_markdown, :embedding
    )
    """
    
    for r in recipes:
        if crawl_chefs and r["source_url"]:
            r["chef"] = extract_chef_from_url(r["source_url"])
        cursor.execute(insert_sql, r)
        
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    
    clean_files = [
        "Recipes_2021_Clean.md",
        "Recipes_2022_Clean.md",
        "Recipes_2023_Clean.md",
        "Recipes_2024_Clean.md",
        "Recipes_2025_Clean.md",
        "Recipes_2026_Clean.md"
    ]
    
    total_loaded = 0
    # Set crawl_chefs=True if you want live HTTP scraping of source URLs for chef metadata
    CRAWL_CHEFS_ENABLED = False 
    
    for cf in clean_files:
        if os.path.exists(cf):
            recipes = parse_cleaned_markdown(cf)
            load_to_db(recipes, crawl_chefs=CRAWL_CHEFS_ENABLED)
            print(f"Loaded {len(recipes)} structured recipes from {cf}")
            total_loaded += len(recipes)
        else:
            print(f"Skipping {cf} (cleaned file not found)")
            
    print(f"Total recipes successfully compiled into {DB_NAME}: {total_loaded}")