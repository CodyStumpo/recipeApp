import os
import re

def clean_markdown_content(raw_text: str) -> str:
    """
    Safely strips out monthly calendar grid tables and trailing header anchor IDs ({#...}),
    while preserving month/year headers and all recipe content.
    """
    lines = raw_text.splitlines()
    cleaned_lines = []
    
    in_calendar = False
    
    for line in lines:
        stripped = line.strip()
        
        # 1. Detect start of a calendar table (weekday header row containing M, W, Su)
        if "|" in stripped and ("M" in stripped and "W" in stripped and "Su" in stripped):
            in_calendar = True
            continue
            
        # 2. If inside a calendar table, skip separator rows and date/grid rows until blank line or non-table line
        if in_calendar:
            if not stripped or not stripped.startswith("|"):
                in_calendar = False
            else:
                continue  # Skip calendar grid row
                
        # 3. Keep valid month/year context headers (e.g., "# December 2021")
        if re.match(r"^#+\s+(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4}", stripped, re.IGNORECASE):
            cleaned_lines.append(line)
            continue
            
        # 4. Skip stray empty headers or standalone '#' symbols left over from cleaning
        if re.match(r"^#+\s*$", stripped) or stripped == "#":
            continue
            
        # 5. Strip trailing header anchor IDs like ` {#linguini-&-clams}` from headers
        if line.strip().startswith("#"):
            line = re.sub(r"\s*\{#.*?\}\s*$", "", line)
            
        cleaned_lines.append(line)
        
    output_text = "\n".join(cleaned_lines)
    # Collapse excessive consecutive blank lines into clean spacing
    output_text = re.sub(r"\n{3,}", "\n\n", output_text)
    return output_text.strip()

def process_markdown_file(input_path: str, output_path: str):
    """
    Reads a raw markdown file, cleans calendar tables and anchors,
    and writes out a clean, standardized markdown file.
    """
    if not os.path.exists(input_path):
        print(f"File not found: {input_path}")
        return
        
    with open(input_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    cleaned_content = clean_markdown_content(content)
    
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(cleaned_content)
        
    print(f"Successfully generated cleaned file: {output_path}")

if __name__ == "__main__":
    markdown_files = [
        "Recipes_2021.md",
        "Recipes_2022.md",
        "Recipes_2023.md",
        "Recipes_2024.md",
        "Recipes_2025.md",
        "Recipes_2026.md"
    ]
    
    for mf in markdown_files:
        if os.path.exists(mf):
            base_name, ext = os.path.splitext(mf)
            output_file = f"{base_name}_Clean{ext}"
            process_markdown_file(mf, output_file)
        else:
            print(f"Skipping {mf} (file not found in working directory)")