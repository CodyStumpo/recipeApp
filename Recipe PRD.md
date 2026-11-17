# **Product Requirements Document (PRD): Personal Ultra-Concise AI Recipe Assistant**

## **1\. Document Overview & Version Control**

* **Project Title:** Personal Ultra-Concise AI Recipe Assistant  
*   
* **Document Version:** 5.1 (v1 Deterministic Vault Browser \+ Post-v1 AI Roadmap)  
*   
* **Status:** Implementation Ready  
*   
* **Target Platform:** iPad & iPhone First (Responsive Web App / iOS Native App)  
* 

## **2\. Executive Summary & Phased Product Vision**

A personal, lightweight recipe vault and culinary assistant built around a curated collection of 576 seasonal, globally minded recipes. The system ingests raw culinary notes via an initial offline batch build and delivers ultra-concise execution blueprints (ratios, heat levels, and timing checkpoints) optimized for an intuitive home cook, eliminating conversational filler and narrative padding.

The product follows a two-stage release trajectory:

* **v1 — Deterministic Recipe Vault Browser (Current Focus):** A fast, zero-AI, iPad- and iPhone-optimized browser over the cleaned recipe vault (recipes\_base.db, 576 recipes). v1 focuses exclusively on frictionless search, multi-select metadata filtering, progressive-disclosure recipe inspection, deterministic complementary dish pairing, and local user star ratings and notes.  
*   
* **Post-v1 (v2+) — AI Discovery, Web Synthesis & Generative Expansion (Future State):** Builds upon the v1 vault foundation to introduce local semantic vector search (Path A+), external multi-source web recipe synthesis (Path B), and generative AI creation of novel seasonal dishes matching the curated collection's vibe and structural constraints (Path C).

## **3\. Problem Statement & Phased Strategic Justification**

* **The Problem:** Standard recipe platforms and food blogs bury core cooking instructions beneath personal essays and SEO filler. Existing personal notes lack standardized metadata, creating search friction and limiting dynamic filtering across varied time constraints and available equipment.  
*   
* **Why Phased Architecture:**  
* 

  * **v1 Immediate Value:** Because the 576-recipe catalog is cleaned, structured, and enriched into a canonical SQLite database (recipes\_base.db) via Phase 1, v1 requires zero runtime LLM latency or inference cost to deliver an instant, reliable kitchen companion.  
  *   
  * **Post-v1 AI Leverage:** Once the v1 vault UX is validated, generative models and vector embeddings will bridge the gap between the user's existing collection and new culinary discovery—finding or synthesizing recipes similar to the curated vault without compromising ultra-concise formatting.  
* 

## **4\. Success Metrics & Performance Benchmarks (KPIs)**

### **4.1 Product & User Experience Metrics**

* **Time-to-Blueprint (v1 Vault):** Sub-500ms client-side filtering, search ranking, and recipe rendering across all 576 recipes on iPad and iPhone.  
*   
* **Time-to-Blueprint (Post-v1 Path A+):** Sub-1.5 second semantic retrieval and rendering of local vault recipes via local vector search.  
*   
* **Path B & C Latency Acceptance (Post-v1):** External web synthesis and generative creation are permitted longer latency (greater than 1.5s) due to external API roundtrips and multi-source synthesis.  
*   
* **Zero Fluff Compliance:** 100% adherence to ultra-concise formatting rules across both v1 blueprints and post-v1 synthesized recipes (no narrative prose, personal essays, or introductory pleasantries).  
* 

### **4.2 Post-v1 AI System & Infrastructure Metrics**

* **Semantic Matching Score & Fallback Routing (v2+):** Retrieval routing is governed by cosine similarity scores against the local vector database:  
* 

  * **High Match (greater than 0.85):** Triggers Path A+ (Curated Vault Semantic Retrieval).  
  *   
  * **Medium Match (0.60–0.84):** Triggers Path B (External Web Retrieval & Synthesis).  
  *   
  * **Low Match (less than 0.60):** Triggers Path C (AI Vibe Synthesis).  
  *   
* **Token Cost Efficiency:** Minimal token overhead per transaction via lightweight model routing for batch metadata extraction and runtime formatting.  
* 

## **5\. User Personas & Core User Journeys**

* **Primary Persona:** The Confident Home Cook. Experienced in the kitchen, treats recipes as execution blueprints, and prioritizes speed, inline quantities, and technical precision over hand-holding.  
*   
* **Core v1 Journey:** User opens the app on iPad or iPhone, enters a search query and/or selects multi-select metadata filters (Dish Type, Subtype, Cuisine, Effort, Season, Vibe, Dietary, Rating), scans a ranked grid of cards with clear visual hierarchy, opens a selected recipe modal to view full metadata, equipment, folded ingredient master list, and execution blueprint, explores complementary dish pairings via in-modal navigation, and logs a 1–5 star rating and personal notes.  
* 

## **6\. System Scope & Content Architecture (The "IS / IS NOT" Boundaries)**

| Dimension | Scope Definition |
| :---- | :---- |
| **What It Is** | A seasonal collection of 576 recipes ranging from quick weeknight dishes to long weekend projects (barbecue, braises, complex curries); global cuisines; ultra-concise execution notes with inline quantities; deterministic v1 vault browser with post-v1 AI discovery. |
| **What It Isn't** | Not a mom blog, a beginner's hand-holding cookbook, a rigid macro-counted meal-prep planner, or an import/export file manager. |

* ## **7\. Release Scope & Future Multi-Path Routing Architecture**

* **v1 Scope — Deterministic Vault Browser:**  
* 

  * **Read-Only Vault Boundary:** The cleaned recipe catalog (recipes\_base.db) is strictly read-only in the client. No import, export, or file upload controls exist in the UI. All user ratings and personal notes are stored exclusively in client-local state (user\_state / localStorage) keyed by recipe\_id.  
  *   
  * **Standalone Indexing & Deterministic Pairing:** All dishes—including sides nested under mains in the raw notes—are indexed as independent standalone records tagged with dish\_type ("main" vs. "side"). In v1, opening any recipe surfaces 3–4 complementary pairings using deterministic history, role/subtype complementarity, and culinary compatibility scoring.  
  *   
* **Post-v1 (v2+) — AI Retrieval, Web Synthesis & Generative Expansion:**  
* **Post-v1 (v2+) — AI Retrieval, Web Synthesis & Generative Expansion:**  
* 

  * **Path A+ (Curated Vault Semantic Retrieval):** Upgrades v1 search with local vector similarity (sqlite-vec on iOS / Wasm vector index on Web) using the pre-computed embedding BLOB column, enabling conceptual queries (e.g., "bright weeknight fish dinner" or "dishes like Larb").  
  *   
  * **Path B (External Web Retrieval & Multi-Source Synthesis):** When searching for specific dishes outside the curated vault, pulls 3–4 authoritative web references, compares competing methodologies (e.g., dry rubs vs. wet marinades), and synthesizes a single best-approach execution blueprint aligned with the collection's vibe. Results are cached locally post-synthesis to prevent session drift.  
  *   
  * **Path C (AI Vibe Synthesis):** Generative creation of novel seasonal recipes modeled on the flavor profiles, structural constraints, and high-rated dishes in the user's curated vault when vault and web matches fall below threshold.  
  *   
  * **Precise Recipe Modification Bounds (v2+):**  
  * 

    * *Allowed:* Minor ingredient substitutions and dietary accommodations (e.g., swapping standard dairy for coconut milk, substituting proteins, or adjusting aromatics) for savory, free-form, or flexible dishes (braises, stir-fries, roasts, curries).  
    *   
    * *Strictly Prohibited:* Never alter proportions, hydration ratios, or chemical ratios for baking, pastry, dough chemistry, curing, or food preservation recipes.

## **8\. Data Pipeline & Automated Metadata Enrichment Schema**

### **8.1 One-Time / Occasional Offline Build Pipeline**

```

[Google Docs Vault] 
       │ (Manual One-Time / Occasional CLI Script)
       ▼
[1. Boundary Filter & Markdown Segmenter] 
       │ 
       ▼
[2. LLM Metadata Extractor & Culinary Reasoner] 
       │ 
       ▼
[3. Pre-Built SQLite + Vector Bundle] ──► [Packaged into Web / iOS App]

```

### **8.2 Ingestion & Enrichment Rules**

* **Step 1: Boundary Filtering & Segmentation:**  
* 

  * **Non-Recipe Filtering:** Automatically discards chronological section headers (e.g., November, October, August) and inventory/scratchpad blocks (e.g., In freezer lists lacking preparation instructions). Monthly calendar grid tables (e.g., \| M \| T \| W \| Th \| F \| Sa \| Su \|) at the beginning of monthly markdown files are completely stripped out during boundary filtering, while month/year context headers (e.g., November 2021\) are retained as temporal anchors for seasonal inference.  
  *   
  * **Heading Decoupling:** Extracts both top-level headings (\#) and sub-headings (\#\#, \#\#\#) as independent recipe records, classifying each as "main" or "side" while preserving an optional historical\_pairing\_id reference without enforcing hard coupling.  
  *   
* **Step 2: Deterministic ID & Upsert Strategy:**  
* 

  * Generates a deterministic recipe\_id from a normalized slug of the recipe title (e.g., rec\_yucatan\_turkey).  
  *   
  * Tracks a source\_content\_hash (SHA-256 of the raw markdown block). If an occasional re-sync occurs and source\_content\_hash changes, the upstream base blueprint updates while preserving all local user ratings, comments, and user-created override layers in separate local tables keyed by recipe\_id.  
  *   
* **Step 3: LLM Metadata Extraction & Normalization:**  
* 

  * **Controlled Vocabularies:** Maps effort\_level strictly to a 4-tier enum ("Low", "Medium", "Medium-High", "High") alongside a brief effort\_rationale string.  
  *   
  * **Unquantified Ingredients & Missing Times:** When raw notes list ingredients without explicit measurements (e.g., Achiote, s\&p, cilantro) or optional items (Maybes: ...), the extractor preserves them in ingredient\_master\_list without hallucinating amounts—implicitly denoting "to taste" or "optional" (annotated clearly for the extractor). Missing marinade or cook durations default to null rather than fabricated numbers.  
  *   
  * **Basic Culinary Reasoning:** Infers implicit non-basic equipment (e.g., wire roasting rack for spatchcocked oven roasting, meat thermometer when target internal temperatures are stated) and frames cook times as planning estimates whenever target temperatures are provided.  
  *   
* **Step 4: Bundle Generation:** Outputs a self-contained SQLite database containing structured JSON records and dense vector embeddings ready for client bundling.  
* 

### **8.3 JSON Metadata Schema**

JSON

```
{
  "recipe_id": "rec_yucatan_turkey",
  "source_content_hash": "a1b2c3d4e5f6...",
  "title": "Yucatan Turkey",
  "dish_type": "main",
  "dish_subtype": null,
  "cuisine": "Yucatan / Mexican",
  "vibe": ["citrusy", "bold", "smoky", "savory"],
  "season": ["autumn", "winter"],
  "dietary_flags": ["dairy-free", "gluten-free"],
  "active_prep_time_minutes": 25,
  "marinade_time": "Overnight",
  "cook_time_minutes": 150,
  "oven_time_minutes": 150,
  "cook_time_attention_minutes": 15,
  "effort_level": "Medium-High",
  "effort_rationale": "Requires spatchcocking poultry, overnight marinating, and dual-stage temperature management.",
  "equipment_needed": [
    "Meat thermometer",
    "Wire roasting rack and sheet pan",
    "Aluminum foil",
    "Optional: Big Green Egg (BGE) smoker with pecan wood"
  ],
  "ingredient_master_list": [
    "1 whole turkey (spatchcocked)",
    "Achiote paste (to taste)",
    "1 cup orange juice",
    "½ cup lime juice",
    "½ cup grapefruit juice (~1 grapefruit)",
    "8 cloves garlic",
    "1 tbsp oregano",
    "1 tsp cumin",
    "1 tsp allspice",
    "1 tsp black pepper",
    "2 tbsp kosher salt",
    "¼ cup olive oil"
  ],
  "historical_pairing_ids": [
    "rec_charred_corn_black_bean_salad",
    "rec_pickled_red_onion",
    "rec_salsa_verde",
    "rec_saffron_rice"
  ],
  "source": null,
  "chef": null
}
```

*(Note: Nutritional information is omitted from the schema.)*

## **9\. Style Enforcement & Prompt Engineering Strategy**

* **9.1 Minimalist Micro-Format Rules:**  
* 

  * **Inline Quantities Only:** No separate top-level ingredient block in the default execution view. All quantities and measurements are embedded directly inline within the imperative action steps (matching the raw training data style).  
  *   
  * **Temperature Over Timers:** Whenever target internal temperatures are specified, cook durations are explicitly framed as planning estimates rather than hard stops.  
  *   
  * **Zero Fluff:** Strict imperative verbs, ratios, heat levels, and timing checkpoints with zero narrative preamble.  
  *   
* **9.2 System Prompt Architecture (Ingestion & Runtime):**  
* 

* Plaintext

```

You are a technical culinary parser and execution formatter.

Apply basic culinary reasoning during extraction and formatting:
1. Implicit Equipment: Infer non-basic gear required by the technique (e.g., wire rack for spatchcocked oven roasting, instant-read thermometer whenever target internal temperatures are stated, Dutch oven for long braises) and include it in `equipment_needed`.
2. Temperature vs. Time: Whenever a target internal temperature is given, explicitly frame cook durations as planning estimates rather than hard stops.
3. Shorthand & Unquantified Items: Normalize abbreviated notes into clear imperative steps with inline quantities. Do not invent measurements for unquantified ingredients (e.g., "s&p", "cilantro", "achiote"); treat unquantified items as "to taste" and list them cleanly without fabricated numbers.
4. Standalone Segmentation: Extract nested side dishes as standalone records tagged `dish_type: "side"`. Ignore non-recipe inventory lists or date headers.

```

*   
* **9.3 Few-Shot Exemplar Set:** Curated input/output pairs derived from the personal Google Docs archive demonstrating shorthand-to-blueprint transformation.  
* 

  * ## **10\. v1 UX & Interface Specification: Deterministic Vault Browser**

### **10.1 Responsive Layout & Navigation (iPad & iPhone First)**

* **Viewport Targets:**  
  * **iPhone (Portrait \< 640px):** Single-column card stack; recipe detail view opens as a full-screen sheet with a sticky top header bar.  
  *   
  * iPad (640px – 1024px): 2-column responsive card grid; detail view opens as a centered modal sheet (max-width: 720px).  
  *   
  * **Desktop (\> 1024px):** 3-column card grid; centered detail modal.  
* **Chrome Constraints:** Clean header with no version badges, subtitles, import/export buttons, or multi-course meal-planner drawers.  
* **Touch Accessibility:** All interactive controls (search, filter dropdowns, tags, star ratings, modal actions) enforce a minimum 44px x 44px tap target.  
* 

### **10.2 Main Page Search & Deterministic Ranking**

* **Search Input:** Prominent top search bar with placeholder text: "Search recipes, ingredients, vibes,...".  
*   
* **Search Scope:** Case-insensitive substring/token matching across title, ingredient\_master\_list\_json, vibe\_json, cuisine, and blueprint\_markdown.  
*   
* **Sort Priority:** Matching recipes are ranked strictly in the following order:  
* 

  * **1\. Search Relevance Score** (when search query is non-empty): Exact/prefix title match (+10) \> title substring (+6) \> vibe/cuisine match (+4) \> ingredient list match (+3) \> blueprint body match (+1).  
  *   
  * **2\. User Star Rating:** Highest user-assigned star rating (5 down to 1, unrated 0 last).  
  *   
  * **3\. Alphabetical:** Ascending by title (A \-\> Z).  
  * 

### **10.3 Multi-Select Filter Strip (8 Dimensions)**

* **Layout Behavior:** Arranged in a compact horizontal strip directly beneath the search bar. On iPhone and portrait iPad viewports, the strip scrolls horizontally with clean edge affordances (avoiding awkward multi-line wrapping); on wide viewports, controls sit on a single row. Includes a conditional "Clear" pill whenever 1 or more filters are active.  
*   
* **Filter Dropdowns:**  
* 

  * **1\. Dish Type:** main, side  
  *   
  * **2\. Subtype:** vegetable, starch, rice, grain, salad, bread, soup, pasta, stir-fry, appetizer, stew, dessert  
  *   
  * **3\. Cuisine:** Dynamically populated from distinct non-null cuisine values  
  *   
  * **4\. Effort:** Low, Medium, Medium-High, High  
  *   
  * **5\. Season:** spring, summer, autumn, winter  
  *   
  * **6\. Vibe:** Dynamically populated with mapped emoji icons  
  *   
  * **7\. Dietary:** Dynamically populated from dietary\_flags\_json  
  *   
  * **8\. Rating:** 5 ★, 4+ ★, 3+ ★, Unrated  
  *   
* **Boolean Logic:**  
* 

  * **Within a single dropdown:** OR logic (e.g., selecting Italian \+ Mexican returns recipes matching either cuisine).  
  *   
  * **Across different dropdowns:** AND logic (e.g., Main AND Low Effort AND Summer).  
  * 

### **10.4 Recipe Card Hierarchy (Collapsed Overview)**

Card elements follow a 3-tier visual hierarchy to prioritize rapid scanning on mobile/tablet screens (omitting any NULL, None, empty, or N/A field cleanly):

* **1\. Primary Anchor (Top & Title):**  
* 

  * Top-left badge: DISH TYPE or DISH TYPE · SUBTYPE (e.g., MAIN · STEW).  
  *   
  * Top-right pill: Effort Level (Low, Medium, Medium-High, High) \+ subtle gold ★ badge if rated by the user.  
  *   
  * **Recipe Title** (high-contrast primary heading) directly above **Cuisine** subtitle.  
  *   
* **2\. Secondary Anchor (Compact Visual Time Strip):**  
* 

  * Displays active vs. passive durations in a unified visual strip:  
  * 

    * **Active Time Group:** Prep \[X\]m and Cook \[Y\]m rendered as primary time badges.  
    *   
    * **Passive Time Group:** Marinade \[Z\] and Oven \[W\]m rendered as muted/outlined secondary badges only when present.  
    *   
* **3\. Tertiary Context (Tags & Footer):**  
* 

  * **Vibe Tags:** Emoji \+ label pills (e.g., 🍯 sweet, 🥩 savory), capped at 4 pills on the card face (+N overflow indicator if more exist).  
  *   
  * **Footer Row:** Compact Season labels/icons \+ Dietary badges on the left; Open \-\> action indicator on the right.  
  * 

### **10.5 Recipe Detail Modal Specification**

Tapping any card opens the full detail view:

* **1\. Sticky Navigation Header:** Displays "\<- Back to \[Previous Recipe Title\]" whenever opened via a pairing link (popping the modal navigation stack on tap), alongside a top-right X close button.  
*   
* **2\. Full Metadata Header:**  
* 

  * Type · Subtype, Cuisine, Effort (plus effort\_rationale callout if present), Seasons, complete Vibe pills (icons \+ words), and complete Dietary flags.  
  *   
  * **Chef & Source Attribution:** Displays By \[Chef\] and/or a clickable "View Source Recipe" external link when source\_url is present.  
  *   
  * **Full Time Breakdown:** Explicit display of Active Prep, Cook Time, Marinade / Rest Time, and Oven Time (omitting null durations).  
  *   
* **3\. Equipment Needed:** Rendered as horizontal pills above the ingredients (omitted if empty).  
*   
* **4\. Ingredient Master List (Folded by Default):**  
* 

  * Positioned directly above the Execution Blueprint.  
  *   
  * Collapsed bar displays Ingredient Master List (\[Count\]) with an Unfold toggle.  
  *   
  * Expanding reveals the clean bulleted ingredient list without interactive checkboxes.  
  *   
* **5\. Execution Blueprint:** Renders blueprint\_markdown with bolded quantities, heat levels, and timing checkpoints, free of checkboxes.  
*   
* **6\. Pairs Well With (Deterministic Pairing Section):**  
* 

  * Displays up to 3–4 clickable pairing pills.  
  *   
  * Tapping a pairing pill pushes the current recipe onto the modal history stack and loads the paired recipe in place.  
  *   
* **7\. User Rating & Notes Footer:**  
* 

  * Interactive 1–5 Star Selector (tapping the active star clears rating back to unrated).  
  *   
  * Auto-saving Personal Notes textarea (user\_state / localStorage persistence keyed by recipe\_id) with subtle "Saved" confirmation feedback.  
  * 

### **10.6 Deterministic Pairing Recommendation Logic (v1)**

When a recipe R is opened in the detail view, candidate recipes C \!= R are ranked via a lightweight 3-tier rule set:

* **1\. Tier 1 — Explicit Historical Pairings:** Any valid recipe\_id in R's historical\_pairing\_ids\_json is placed first.  
*   
* **2\. Tier 2 — Role & Subtype Complementarity:**  
* 

  * If R is a main, eligible candidates must have dish\_type \= 'side'.  
  *   
  * If R is a side, eligible candidates must have dish\_type \= 'main' (or a contrasting side subtype such as salad \<-\> starch/rice).  
  *   
  * **Duplicate Subtype Exclusion:** Candidates sharing the exact same non-null dish\_subtype as R are excluded (e.g., never pair a pasta main with a pasta side).  
  *   
* **3\. Tier 3 — Culinary Compatibility Score (Fills Remaining Slots up to 4 Total):**  
* 

  * **Cuisine Match (+3 pts):** Exact match on cuisine (or regional affinity, e.g., Sichuan \<-\> Chinese).  
  *   
  * **Dietary Preservation (+2 pts):** Candidate satisfies all dietary\_flags present on R.  
  *   
  * **Vibe Contrast Bonus (+2 pts):** If R features rich/heavy vibes (rich, creamy, heavy, savory), boost candidates with balancing vibes (fresh, bright, tangy, crisp, citrusy), and vice versa.  
  *   
  * **Season Overlap (+1 pt):** Shares at least one active season with R.  
  *   
  * **Oven Collision Penalty (-2 pts):** Applied if both R and candidate C require oven cooking (oven\_time\_minutes \> 0\) to prevent simultaneous oven/temperature conflicts.  
  *   
  * **Tie-Breaker:** Higher user star rating, then alphabetical by title.

## **11\. Technical Architecture & Local Storage Spec**

* **Offline Build & Bundle Distribution:** Because vault extraction runs once (or rarely via manual CLI script), Google Drive authentication, markdown parsing, LLM extraction, and embedding generation occur offline in a standalone Python build script. The script compiles a read-only base SQLite bundle (recipes\_base.db) containing the structured metadata and vector embeddings, which is packaged directly into the Web and iOS clients.  
*   
* **SQLite Database Schema Spec:** The main recipes table enforces binary dish\_type constraints (CHECK(dish\_type IN ('main', 'side'))) alongside categorized dish\_subtype values (CHECK(dish\_subtype IN ('vegetable', 'starch', 'rice', 'grain', 'salad', 'bread', 'soup', 'pasta', 'stir-fry', 'appetizer', 'stew', 'dessert'))). Additional structured columns include integer durations like oven\_time\_minutes INTEGER, while redundant scalar text columns (vibe, season, dietary\_flags, prep\_time, cook\_time) are removed to favor normalized structured integer/JSON fields.  
*   
* **Client Local State (iOS & Web):**  
* 

  * **iOS:** Native SQLite (via GRDB / SQLite.swift) \+ sqlite-vec for sub-second offline vector similarity search.  
  *   
  * **Web:** Wasm SQLite (sql.js / OPFS) \+ client-side vector similarity search.  
  *   
  * **User State Overlay:** Local ratings, comments, recipe modifications, and cached Path B/C results are stored in a dedicated user\_state table keyed by recipe\_id, completely decoupled from the read-only recipes\_base.db bundle.  
  * 

## **12\. AI Guardrails, Safety & Regulatory Constraints**

* **Food Safety Baselines:** Strict enforcement of safe minimum internal cooking temperatures (e.g., 165°F poultry) and proper food handling guidance.  
*   
* **Modification Safety Guardrails:** Hard block on ratio modifications for baking, pastry, and preservation recipes.  
*   
* **Scope Restriction:** Immediate rejection of non-culinary queries.  
* 

## **13\. Automated AI Evaluation (Eval) Framework**

* **13.1 Evaluation Test Dataset:** Benchmark suite covering quick weeknight assemblies, complex multi-stage weekend projects, implicit equipment inference cases, standalone side pairing, and dietary-adjusted queries.  
*   
* **13.2 Metric Rubrics:**  
* 

  * **Format & Conciseness:** Validates inline quantities, absence of top-level ingredient lists, preservation of unquantified "to taste" items without hallucination, and zero mom-blog filler.  
  *   
  * **Culinary Reasoning Accuracy:** Verifies implicit equipment detection and temperature-anchored timing framing.  
  *   
  * **Vibe Alignment:** Evaluates whether Path B (web synthesis) and Path C (generative) outputs match the tone, flavor profile, and technical directness of the original Google Docs vault.  
  *   
* **13.3 LLM-as-a-Judge:** Automated validation pipeline scoring outputs against the rubrics prior to prompt or model updates.  
* 

## **14\. System Architecture, Model Selection & Unit Economics**

* **14.1 Model Tiering Strategy:**  
* 

  * *Lightweight Frontier / Fast Models:* One-time batch metadata extraction, JSON schema mapping, and simple Path A formatting.  
  *   
  * *High-Capability Frontier Models:* Path B multi-source web synthesis, dietary adaptation reasoning, and Path C novel dish generation.  
  *   
* **14.2 Token Budget:** Near-zero ongoing ingestion cost due to one-time offline bundle generation; minimal runtime context window usage by retrieving only top\-$k$ vector matches and compact JSON metadata payloads.  
* 

## **15\. Implementation Roadmap & Release Phases**

* **Phase 1: Offline Ingestion & Bundle Builder:** Build the offline Python CLI pipeline to clean markdown, extract standalone mains/sides into the JSON schema, crawl source URLs for chef metadata, augment metadata via LLM, generate embeddings, and compile recipes\_base.db (576 curated recipes).  
*   
* **Phase 2 (v1 Release): Deterministic Recipe Vault Browser (iPad & iPhone First):** Build the zero-AI, responsive client app over recipes\_base.db featuring real-time search ranking, 8-dimension multi-select filtering, 3-tier progressive disclosure cards, detail modal with folded ingredient list and execution blueprint, 3-tier deterministic dish pairing with modal history navigation, and local 1–5 star rating and personal notes persistence.  
*   
* **Phase 3 (v2+ Release): AI Semantic Search, Web Synthesis & Generative Discovery:** Layer in local vector similarity search (Path A+ via sqlite-vec / Wasm), external multi-source web retrieval and synthesis (Path B), and generative AI creation of novel seasonal recipes modeled on the curated vault (Path C).  
* 

