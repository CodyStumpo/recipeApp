import sqlite3
import json

DB_PATH = "recipes_base.db"
JSON_OUT = "recipes_export.json"
MD_OUT = "recipes_export.md"

def export_database():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Exclude binary embedding BLOBs so the exported files remain clean text
    cursor.execute("""
        SELECT recipe_id, title, dish_type, dish_subtype, cuisine,
               vibe_json, season_json, dietary_flags_json,
               active_prep_time_minutes, marinade_time, cook_time_minutes,
               cook_time_attention_minutes, oven_time_minutes,
               effort_level, effort_rationale, equipment_needed_json,
               ingredient_master_list_json, source_url, chef,
               historical_pairing_ids_json, blueprint_markdown
        FROM recipes
        ORDER BY title ASC
    """)
    
    rows = cursor.fetchall()
    recipes_list = []

    json_cols = {
        "vibe_json", "season_json", "dietary_flags_json",
        "equipment_needed_json", "ingredient_master_list_json",
        "historical_pairing_ids_json"
    }

    for row in rows:
        item = dict(row)
        for col in json_cols:
            if item[col]:
                try:
                    item[col] = json.loads(item[col])
                except Exception:
                    pass
        recipes_list.append(item)

    # 1. Export clean JSON (ideal for loading directly into your web app)
    with open(JSON_OUT, "w", encoding="utf-8") as f:
        json.dump(recipes_list, f, indent=2, ensure_ascii=False)

    # 2. Export readable Markdown (ideal for uploading to this Notebook)
    with open(MD_OUT, "w", encoding="utf-8") as f:
        f.write("# Recipe Database Export\n\n")
        for r in recipes_list:
            f.write(f"## {r['title']} (`{r['recipe_id']}`)\n")
            f.write(f"- **Type:** {r['dish_type']} ({r['dish_subtype'] or 'standard'})\n")
            f.write(f"- **Cuisine:** {r['cuisine'] or 'N/A'} | **Effort:** {r['effort_level'] or 'N/A'}\n")
            if r['season_json']:
                f.write(f"- **Seasons:** {', '.join(r['season_json'])}\n")
            if r['vibe_json']:
                f.write(f"- **Vibe:** {', '.join(r['vibe_json'])}\n")
            if r['dietary_flags_json']:
                f.write(f"- **Dietary:** {', '.join(r['dietary_flags_json'])}\n")
            f.write(f"- **Times (min):** Prep: {r['active_prep_time_minutes']}, Cook: {r['cook_time_minutes']}, Oven: {r['oven_time_minutes']}\n")
            if r['chef'] or r['source_url']:
                f.write(f"- **Source:** {r['chef'] or ''} ({r['source_url'] or ''})\n")
            if r['ingredient_master_list_json']:
                f.write(f"- **Ingredients:** {', '.join(r['ingredient_master_list_json'])}\n")
            f.write("\n### Blueprint\n")
            f.write(f"{r['blueprint_markdown'] or ''}\n\n---\n\n")

    conn.close()
    print(f"Exported {len(recipes_list)} recipes to {JSON_OUT} and {MD_OUT}.")

if __name__ == "__main__":
    export_database()