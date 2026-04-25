
import sys
import time
from pathlib import Path
from patchright.sync_api import sync_playwright

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

from auth_manager import AuthManager
from browser_utils import BrowserFactory

def explore_notebook(notebook_url: str):
    auth = AuthManager()
    if not auth.is_authenticated():
        print("Not authenticated")
        return

    playwright = sync_playwright().start()
    context = BrowserFactory.launch_persistent_context(playwright, headless=True)
    page = context.new_page()
    
    print(f"Opening {notebook_url}...")
    try:
        page.goto(notebook_url, wait_until="domcontentloaded", timeout=60000)
        print("  ✓ Page loaded (domcontentloaded)")
    except Exception as e:
        print(f"  ⚠️ Error loading page: {e}")
    
    time.sleep(10) # Wait for UI to settle
    
    # Save screenshot to see current state
    screenshot_path = Path(__file__).parent.parent / "notebook_exploration.png"
    page.screenshot(path=str(screenshot_path))
    print(f"Screenshot saved to {screenshot_path}")
    
    # List buttons and their texts
    buttons = page.query_selector_all("button")
    print("\nButtons found:")
    for i, btn in enumerate(buttons):
        try:
            text = btn.inner_text().strip()
            if text:
                print(f"{i}: {text}")
        except:
            pass

    context.close()
    playwright.stop()

if __name__ == "__main__":
    explore_notebook("https://notebooklm.google.com/notebook/61967307-842b-4d61-a782-11bd69d2004b")
