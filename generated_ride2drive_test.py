from playwright.sync_api import sync_playwright
from self_healing import SelfHealingPage
import time

def run():
    print('Starting generated test...')
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        raw_page = browser.new_page()
        page = SelfHealingPage(raw_page)
        page.goto('https://r2d-au-dev.vercel.app/')
        time.sleep(2)


        # Potential buttons to click (uncomment to use):
        # page.click("text=Types of Vehicles")
        # page.click("text=Vehicle Brands")
        # page.click("text=Who pays for the accident loan car?")
        # page.click("text=What happens if the at fault insurer doesn't pay the bill?")
        # page.click("text=Am I eligible for an accident loan car if the accident wasn’t my fault and I don’t have any insurance?")
        # page.click("text=I was rear-ended yesterday. Can I get an accident loan car?")
        # page.click("text=Is Right2Drive related to my insurance company or any other insurance company?")

        browser.close()

if __name__ == '__main__':
    run()