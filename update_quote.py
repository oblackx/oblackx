#!/usr/bin/env python3
"""
Update the 'Thought of the Day' section in README.md with a random quote from quotes.json.
Uses the readme-daily-quotes.vercel.app API (same as Kiran1689).
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
    """Update the README.md with the new quote card."""
    readme_path = Path("README.md")
    content = readme_path.read_text(encoding="utf-8")

    # Format the quote card using readme-daily-quotes API (same as Kiran1689)
    quote_text = quote['text'].replace(' ', '%20').replace(',', '%2C').replace('.', '%2E').replace("'", '%27')
    author_text = quote['author'].replace(' ', '%20')

    card_design = f'''<!--STARTS_HERE_QUOTE_CARD-->
<p align="center">
    <img src="https://readme-daily-quotes.vercel.app/api?author={author_text}&quote={quote_text}&theme=dark&bg_color=1a1b27&author_color=36BCF7&accent_color=36BCF7">
</p>
<!--ENDS_HERE_QUOTE_CARD-->'''

    today = datetime.utcnow().strftime("%b %d, %Y")

    # Replace the quote card (between START and END markers)
    pattern = r'<!--STARTS_HERE_QUOTE_CARD-->(.|\n)*?<!--ENDS_HERE_QUOTE_CARD-->'
    new_content = re.sub(pattern, card_design, content, flags=re.DOTALL)

    # Update the "Last updated" date
    new_content = re.sub(
        r'\*Last updated: <!--QUOTE_DATE-->\*',
        f'*Last updated: {today}*',
        new_content
    )

    if new_content == content:
        print("WARNING: Could not find quote section to replace!")
        return False

    readme_path.write_text(new_content, encoding="utf-8")
    print(f"Updated quote: \"{quote['text']}\" — {quote['author']}")
    print(f"Date: {today}")
    return True

def main():
    quotes = load_quotes()
    quote = pick_random_quote(quotes)
    success = update_readme(quote)
    if not success:
        exit(1)

if __name__ == "__main__":
    main()