import json

HTML_PATH = "index.html"
JSON_PATH = "recipes_export.json"

with open(HTML_PATH, "r", encoding="utf-8") as f:
    html = f.read()

with open(JSON_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

# Escape any '</' sequences (such as '</script>') so the HTML parser never prematurely closes the script block
safe_json = json.dumps(data, ensure_ascii=False).replace("</", r"<\/")

start = html.index("const RECIPES =")
end = html.index("const FALLBACK_RECIPES =")

html_new = html[:start] + "const RECIPES = " + safe_json + ";\n\n    " + html[end:]

with open(HTML_PATH, "w", encoding="utf-8") as f:
    f.write(html_new)

print(f"Done! {len(data)} recipes injected cleanly ({len(html_new)} bytes).")
