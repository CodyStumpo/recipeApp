import sqlite3
import json
import os
import time
from typing import Optional
from google import genai
from google.genai import types

DB_NAME = "recipes_base.db"

# Initialize the Gemini client (expects GEMINI_API_KEY environment variable to be set)
client = genai.Client()

AUGMENTATION_PROMPT = """
You are a technical culinary parser and metadata extractor. 
Analyze the following recipe blueprint and extract/infer structured metadata according to these strict rules:

1. dish_type: Strictly either "main" (standalone centerpieces, one-dish meals, complete proteins) or "side" (accompaniments cooked alongside a main).
2. dish_subtype: Choose strictly from ('vegetable', 'starch', 'rice', 'grain', 'salad', 'bread', 'soup', 'pasta', 'stir-fry', 'appetizer', 'stew', 'dessert') or null if it's a standard protein main/roast.
3. cuisine: Identify the culinary origin or style (e.g., "Italian", "Mexican", "Persian", "American").
4. vibe_json: JSON array of flavor profile strings (e.g., ["citrusy", "bold", "smoky", "savory"]).
5. season_json: JSON array of appropriate seasons ("spring", "summer", "autumn", "winter"), informed by the provided preparation month context and ingredient profile.
6. dietary_flags_json: JSON array of dietary attributes (e.g., ["dairy-free", "gluten-free", "vegetarian"]).
7. active_prep_time_minutes: Integer minutes for hands-on prep.
8. marinade_time: String description of resting/marinating duration if applicable (e.g., "Overnight", "1-4 hours", null).
9. cook_time_minutes: Total active/passive cooking duration in minutes (integer or null).
10. oven_time_minutes: Total time spent cooking in the oven in minutes (integer or null). Useful for hot-day constraints.
11. cook_time_attention_minutes: Active hands-on attention time during cooking (integer or null).
12. effort_level: Strictly one of ("Low", "Medium", "Medium-High", "High").
13. effort_rationale: Short explanatory string justifying the effort level.
14. equipment_needed_json: JSON array of specialized/non-basic gear required by the technique (e.g., ["Meat thermometer", "Wire roasting rack"]). Do not list basic pots/pans/knives.
15. ingredient_master_list_json: JSON array of all ingredients with normalized inline quantities. Keep unquantified items ("s&p", "cilantro", "achiote") as "to taste" without hallucinating numbers.

Recipe Title: {title}
Context Preparation Month: {season_context}
Recipe Blueprint:
{blueprint}
"""

def augment_recipes(db_path: str = DB_NAME):
    if not os.path.exists(db_path):
        print(f"Database not found at {db_path}. Please run your parsing script first.")
        return

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    # Fetch recipes that haven't been augmented yet (where cuisine is still NULL)
    cursor.execute("SELECT recipe_id, title, dish_type, season_json, blueprint_markdown FROM recipes WHERE cuisine IS NULL")
    rows = cursor.fetchall()
    
    print(f"Found {len(rows)} recipes needing LLM metadata augmentation.")
    
    update_sql = """
    UPDATE recipes SET
        dish_type = :dish_type,
        dish_subtype = :dish_subtype,
        cuisine = :cuisine,
        vibe_json = :vibe_json,
        season_json = :season_json,
        dietary_flags_json = :dietary_flags_json,
        active_prep_time_minutes = :active_prep_time_minutes,
        marinade_time = :marinade_time,
        cook_time_minutes = :cook_time_minutes,
        cook_time_attention_minutes = :cook_time_attention_minutes,
        oven_time_minutes = :oven_time_minutes,
        effort_level = :effort_level,
        effort_rationale = :effort_rationale,
        equipment_needed_json = :equipment_needed_json,
        ingredient_master_list_json = :ingredient_master_list_json
    WHERE recipe_id = :recipe_id
    """
    
    for row in rows:
        recipe_id = row["recipe_id"]
        title = row["title"]
        default_dish_type = row["dish_type"]
        
        # Clean up season_json representation for prompt context string
        raw_season = row["season_json"]
        if raw_season:
            try:
                parsed_list = json.loads(raw_season)
                season_context = ", ".join(parsed_list) if isinstance(parsed_list, list) else str(raw_season)
            except Exception:
                season_context = str(raw_season)
        else:
            season_context = "Unknown"
            
        blueprint = row["blueprint_markdown"]
        prompt = AUGMENTATION_PROMPT.format(title=title, season_context=season_context, blueprint=blueprint)
        
        print(f"Augmenting: {title} ...", end=" ", flush=True)
        
        success = False
        # Retry loop: 1 initial attempt + 1 retry = 2 total attempts max
        for attempt in range(2):
            try:
                response = client.models.generate_content(
                    model="gemini-3.8-flash",
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        response_mime_type="application/json",
                        response_schema={
                            "type": "OBJECT",
                            "properties": {
                                "dish_type": {"type": "STRING", "enum": ["main", "side"]},
                                "dish_subtype": {"type": "STRING", "nullable": True},
                                "cuisine": {"type": "STRING", "nullable": True},
                                "vibe_json": {"type": "ARRAY", "items": {"type": "STRING"}, "nullable": True},
                                "season_json": {"type": "ARRAY", "items": {"type": "STRING"}, "nullable": True},
                                "dietary_flags_json": {"type": "ARRAY", "items": {"type": "STRING"}, "nullable": True},
                                "active_prep_time_minutes": {"type": "INTEGER", "nullable": True},
                                "marinade_time": {"type": "STRING", "nullable": True},
                                "cook_time_minutes": {"type": "INTEGER", "nullable": True},
                                "oven_time_minutes": {"type": "INTEGER", "nullable": True},
                                "cook_time_attention_minutes": {"type": "INTEGER", "nullable": True},
                                "effort_level": {"type": "STRING", "enum": ["Low", "Medium", "Medium-High", "High"]},
                                "effort_rationale": {"type": "STRING", "nullable": True},
                                "equipment_needed_json": {"type": "ARRAY", "items": {"type": "STRING"}, "nullable": True},
                                "ingredient_master_list_json": {"type": "ARRAY", "items": {"type": "STRING"}, "nullable": True}
                            },
                            "required": ["dish_type", "effort_level"]
                        },
                        temperature=0.1,
                        http_options={'timeout': 30000} # 30-second timeout in milliseconds
                    )
                )
                
                data = json.loads(response.text)
                
                params = {
                    "recipe_id": recipe_id,
                    "dish_type": data.get("dish_type", default_dish_type),
                    "dish_subtype": data.get("dish_subtype"),
                    "cuisine": data.get("cuisine"),
                    "vibe_json": json.dumps(data.get("vibe_json")) if data.get("vibe_json") else None,
                    "season_json": json.dumps(data.get("season_json")) if data.get("season_json") else raw_season,
                    "dietary_flags_json": json.dumps(data.get("dietary_flags_json")) if data.get("dietary_flags_json") else None,
                    "active_prep_time_minutes": data.get("active_prep_time_minutes"),
                    "marinade_time": data.get("marinade_time"),
                    "cook_time_minutes": data.get("cook_time_minutes"),
                    "cook_time_attention_minutes": data.get("cook_time_attention_minutes"),
                    "oven_time_minutes": data.get("oven_time_minutes"),
                    "effort_level": data.get("effort_level", "Medium"),
                    "effort_rationale": data.get("effort_rationale"),
                    "equipment_needed_json": json.dumps(data.get("equipment_needed_json")) if data.get("equipment_needed_json") else None,
                    "ingredient_master_list_json": json.dumps(data.get("ingredient_master_list_json")) if data.get("ingredient_master_list_json") else None
                }
                
                cursor.execute(update_sql, params)
                conn.commit()
                print("Success.")
                success = True
                break
                
            except Exception as e:
                if attempt == 0:
                    print(f"(Retry after error: {e})", end=" ", flush=True)
                    time.sleep(2)
                else:
                    print(f"Failed permanently: {e}")
                    
        if not success:
            print(f"Skipping recipe {title} due to persistent errors.")
            
    conn.close()
    print("Metadata augmentation complete.")

if __name__ == "__main__":
    augment_recipes()
