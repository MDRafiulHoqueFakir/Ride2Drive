from playwright.sync_api import sync_playwright
from self_healing import SelfHealingPage
import sys

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = SelfHealingPage(browser.new_page())
        
        print("Navigating...")
        page.goto("https://r2d-au-dev.vercel.app/")
        
        print("Attempting to fill with broken selector (timeout=5s)...")
        try:
            # Short timeout to fail fast
            page.fill("#wrongLastName", "Healed Value", timeout=5000)
            print("Fill command completed.")
        except Exception as e:
            print(f"Caught exception in main: {e}")
            
        browser.close()

if __name__ == "__main__":
    run()
