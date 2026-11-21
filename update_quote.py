#!/usr/bin/env python3
"""
Update the 'Thought of the Day' section in README.md with a random quote from quotes.json.
This script is run daily via GitHub Actions.
"""

import json
import random
import re
from datetime import datetime
from pathlib import Path

def load_quotes():
    """Load quotes from quotes.json."""
    with open("quotes.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    return data["quotes"]

def pick_random_quote(quotes):
    """Pick a random quote from the list."""
    return random.choice(quotes)

def update_readme(quote):
    """Update the README.md with the new quote."""
    readme_path = Path("README.md")
    content = readme_path.read_text(encoding="utf-8")

    # Format the quote
    quote_text = f"> **_{quote['text']}_**\n\n> — **{quote['author']}**"
    today = datetime.utcnow().strftime("%B %d, %Y")

    # Replace the quote block (between "> **_This quote updates daily..." and "*Last updated:")
    # Pattern matches the entire quote section
    pattern = r'(> \*\*_This quote updates daily via GitHub Actions_\*\*\n\n)(.*?)(\n\n\*Last updated: <!--QUOTE_DATE-->\*)'

    replacement = rf'\1{quote_text}\n\n*Last updated: {today} UTC*'

    new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)

    if new_content == content:
        # Fallback: try a more specific pattern
        pattern2 = r'(> \*\*_This quote updates daily via GitHub Actions_\*\*\n\n```text\n)(.*?)(\n```\n\n\*Last updated: <!--QUOTE_DATE-->\*)'
        replacement2 = rf'\1{quote["text"]} — {quote["author"]}\3'
        new_content = re.sub(pattern2, replacement2, content, flags=re.DOTAND)

    if new_content == content:
        print("WARNING: Could not find quote section to replace!")
        return False

    readme_path.write_text(new_content, encoding="utf-8")
    print(f"Updated quote: \"{quote['text']}\" — {quote['author']}")
    print(f"Date: {today} UTC")
    return True

def main():
    quotes = load_quotes()
    quote = pick_random_quote(quotes)
    success = update_readme(quote)
    if not success:
        exit(1)

if __name__ == "__main__":
    main()