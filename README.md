# recipeApp
This app contains 576 recipes I have cooked in the last 6 years. The recipes are optimized for use in the kitchen by someone that knows basic techniques and has some culinary judgment.  The point of this is a) a curated collection of recipes I personally found interesting and might want to make again and b) maximized for usability during cooking.

The recipes were highly unstructured and had no meta-data. I used AI to write some python scripts for cleaning and called to LLM for enhancement with meta-data.
The app runs off that data.
If you load the index.html on your device, it will have all the data, and you can make your own personal ratings and notes on the recipes that will persist on that device.
The app will also suggest a few sides to go with a main and vice versa based on some heuristics on the meta-data.

## Possible Future enhancements
* More data cleanup & restoration
* For any search:
  * Include live web search to find recipes I would be likely to curate in, consolidate across top hits to create best version
  * Include generated recipes I would be likely to curate in
  * Build test suite, deterministic + LLM as judge
  * Architect for phase 2 
