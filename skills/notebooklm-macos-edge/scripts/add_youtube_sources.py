
import sys
import time
from pathlib import Path
from patchright.sync_api import sync_playwright

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from auth_manager import AuthManager
from browser_utils import BrowserFactory, StealthUtils

def add_youtube_sources(notebook_url: str, youtube_urls: list):
    auth = AuthManager()
    if not auth.is_authenticated():
        print("Not authenticated")
        return

    playwright = sync_playwright().start()
    context = BrowserFactory.launch_persistent_context(playwright, headless=True)
    page = context.new_page()
    
    print(f"Opening {notebook_url}...")
    page.goto(notebook_url, wait_until="domcontentloaded", timeout=60000)
    time.sleep(10) # Wait for UI to settle

    for i, url in enumerate(youtube_urls):
        print(f"[{i+1}/{len(youtube_urls)}] Adding URL: {url}")
        try:
            # 1. Click "Add sources" if modal not open
            # Check if "YouTube" or "Websites" button is visible already
            website_btn = page.locator("button").filter(has_text="Websites")
            if not website_btn.is_visible():
                add_sources_btn = page.get_by_role("button", name="Add sources")
                if add_sources_btn.is_visible():
                    add_sources_btn.click()
                    time.sleep(3)

            # 2. Click "Websites"
            website_btn = page.locator("button").filter(has_text="Websites")
            # If still not visible, try other variants
            if not website_btn.is_visible():
                website_btn = page.get_by_role("button", name=re.compile("Websites", re.I))
            
            website_btn.click(force=True)
            time.sleep(3)

            # 3. Enter URL
            # The input might be in a dialog
            url_input = page.get_by_placeholder("Insert link")
            if not url_input.is_visible():
                url_input = page.locator("input[type='url']")
            
            url_input.fill(url)
            time.sleep(1)
            
            # 4. Click "Insert"
            insert_btn = page.get_by_role("button", name="Insert")
            if not insert_btn.is_visible():
                # Try by text
                insert_btn = page.locator("button").filter(has_text="Insert")
            
            insert_btn.click()
            print(f"  ✓ Inserted {url}")
            
            # Wait for it to be added and modal to close or stabilize
            time.sleep(5)
            
        except Exception as e:
            print(f"  ❌ Error adding {url}: {e}")
            page.screenshot(path=f"error_adding_{i}.png")
            # Try to escape or close any open dialogs if they are stuck
            page.keyboard.press("Escape")
            time.sleep(2)

    context.close()
    playwright.stop()

if __name__ == "__main__":
    import json
    import argparse
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", required=True)
    parser.add_argument("--file", required=True)
    parser.add_argument("--limit", type=int, default=50)
    args = parser.parse_args()
    
    with open(args.file, 'r') as f:
        urls = [line.strip() for line in f if line.strip()]
    
    # Take only up to the limit
    urls_to_add = urls[:args.limit]
    
    add_youtube_sources(args.url, urls_to_add)
