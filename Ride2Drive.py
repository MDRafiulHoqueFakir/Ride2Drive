# playwright_button_clicks.py
from playwright.sync_api import sync_playwright
import time
import random
import string
from self_healing import SelfHealingPage

def run():
    with sync_playwright() as p:
        # Launch browser (headless=False to see it in action)
        browser = p.chromium.launch(headless=False, slow_mo=500)
        raw_page = browser.new_page()
        page = SelfHealingPage(raw_page)

        # Maximize the browser window
        page.context.new_cdp_session(raw_page).send("Browser.setWindowBounds", {
            "windowId": page.context.new_cdp_session(raw_page).send("Browser.getWindowForTarget")["windowId"],
            "bounds": {"windowState": "maximized"}
        })
        # Go to the website
        url = "https://r2d-au-dev.vercel.app/"
        page.goto(url)

        # Check if the page has loaded by inspecting title or a known element, then print
        if "r2d" in page.title().lower() or page.url == url:
            print("Successfully reached")

        # Wait for the page to load
        page.wait_for_load_state("networkidle")
        # Click the "How it works" button
        how_it_works_button = page.query_selector('header div:nth-child(2) a:nth-child(1)').click()
        # Click the "About us" button
        about_us_button = page.query_selector("//a[normalize-space()='About Us']").click()
        #Click "FAQ" bugtton 
        page.query_selector("//a[normalize-space()='FAQ']").click()
        #Click "Check Eligibility" button
        page.query_selector("//a[normalize-space()='Check Eligibility']").click()
        #Click the "Article" button
        page.query_selector("//a[normalize-space()='Articles']").click()
        #Click the "Apply Now" button
        page.query_selector("//a[normalize-space()='Apply Now']").click()
        time.sleep(2)
       
        # #1st Page(Your Details)
        # #First Name:
        page.fill("input#firstName", "Rafiul")
        time.sleep(1)
        #Last Name:
        # INTENTIONAL BREAK: Changed selector to #wrongLastName to test self-healing
        # print("Testing Self-Healing on Last Name field...")
        # page.fill("input#wrongLastName", "Turjo")
        page.fill("input#lastName", "Turjo")
        time.sleep(1)
        #Email:
        # Generate a random email without any number at the start
        def generate_random_email():
            # Ensure the first character is a letter
            first_char = random.choice(string.ascii_lowercase)
            rest = ''.join(random.choices(string.ascii_lowercase + string.digits, k=7))
            username = first_char + rest
            domain = ''.join(random.choices(string.ascii_lowercase, k=5))
            return f"{username}@{domain}.com"
        random_email = generate_random_email()
        page.fill("input#email", random_email)
        time.sleep(1)
        #Phone Number:
        page.fill("input#phone", "0415789585")
        time.sleep(1)
        #State:
        # Input State
        page.select_option("select#state", "NSW")
        time.sleep(1)
        #Accident Date:
        # Input Accident Date
        page.fill("input#accidentDate", "28/08/2025")
        time.sleep(1)
        #How Did the Collision Occur?
        page.fill("textarea#collision", "Some collision description")
        time.sleep(1)
        #When Do You Need the Car? 
        page.fill("input#carNeedDate", "30/11/2025")
        time.sleep(1)
        #How Did You Hear About Us?
        page.select_option("select#hear", "Google")
        time.sleep(1)
        #Checkbox:
        page.check("input#newsletter")
        time.sleep(1)
        #Submit:
        page.click("#submitBtn")
        time.sleep(1)
        #Click Submit Btn again:
        # Click Submit
        # page.click("#submitBtn")
        # Wait explicitly for an element from Page 2 to appear
        try:
            page.wait_for_selector("input#dob", timeout=20000)
        except Exception:
            print("Page 2 not loaded yet. Checking if we are still on Page 1...")
            if page.is_visible("#submitBtn"):
                print("Retrying Submit Button click...")
                page.click("#submitBtn")
                page.wait_for_selector("input#dob", timeout=30000)
            else:
                raise
        
        # Attempt to wait for a reCaptcha iframe
        try:
            time.sleep(4)
            recaptcha_frame = None
            frames = page.query_selector_all("iframe")
            for frame in frames:
                src = frame.get_attribute("src") or ""
                title = frame.get_attribute("title") or ""
                if "recaptcha" in src.lower() or "recaptcha" in title.lower():
                    recaptcha_frame = frame
                    break
            if recaptcha_frame:
                checkbox = page.frame_locator("iframe[title*='reCAPTCHA']").locator(".recaptcha-checkbox-border")
                checkbox.click(timeout=10000)
                time.sleep(4)
        except Exception as e:
            pass

        #Page 2(Vehicle & Insurance):
        #Date Of Birth:
        page.fill("input#dob", "01/01/1990")
        time.sleep(1)
        #Address:
        page.fill("input#address", "123 Main Street")
        time.sleep(1)
        page.wait_for_selector(".px-3.py-2.cursor-pointer.hover\\:bg-gray-100", timeout=5000)
        page.click(".px-3.py-2.cursor-pointer.hover\\:bg-gray-100")
        time.sleep(3)
        #Your Vehicle Rego State
        page.click("#regoState")
        time.sleep(0.5)
        page.select_option("#regoState", "NSW")
        time.sleep(1)
        #Vehicle Registration Number:
        page.fill("input#registrationNumber", "DK36KT")
        time.sleep(1)
        #Check Vehicle Btn:
        page.click("#checkVehicle")
        time.sleep(1)
        #Insurance Details
        page.click("#vehicleInsuranceIsInsuredYes")
        time.sleep(1)
        #Insurer:
        page.click("#vehicleInsuranceInsurer")
        time.sleep(1)
        page.keyboard.press("ArrowDown")
        time.sleep(0.5)
        page.keyboard.press("Enter")
        time.sleep(1)
        #Claim Number:
        page.fill("#vehicleInsurancePolicyNumber", "111111")
        time.sleep(1)
        def safe_transition(submit_btn_selector, next_page_element_selector, timeout=20000):
            try:
                msg = f"Attempting transition: Click {submit_btn_selector} -> Wait for {next_page_element_selector}"
                print(msg.encode('ascii', 'replace').decode('ascii'))
            except:
                pass

            # Initial click
            if page.is_visible(submit_btn_selector):
                page.click(submit_btn_selector)
            
            try:
                page.wait_for_selector(next_page_element_selector, timeout=timeout)
            except Exception:
                try:
                    msg = f"Next page element {next_page_element_selector} not found. Checking if we are still on previous page..."
                    print(msg.encode('ascii', 'replace').decode('ascii'))
                except:
                    pass

                if page.is_visible(submit_btn_selector):
                    try:
                        msg = f"Retrying click on {submit_btn_selector}..."
                        print(msg.encode('ascii', 'replace').decode('ascii'))
                    except:
                        pass
                    page.click(submit_btn_selector)
                    page.wait_for_selector(next_page_element_selector, timeout=30000)
                else:
                    try:
                        msg = f"Submit button {submit_btn_selector} not visible anymore. Maybe transition happened but element is different?"
                        print(msg.encode('ascii', 'replace').decode('ascii'))
                    except:
                        pass
                    raise
            except Exception as e:
                print(f"Transition failed. Current URL: {page.url}")
                # Print some page text to see if there are errors
                try:
                    content = page.inner_text("body")
                    print(f"Page text sample: {content[:500].encode('ascii', 'replace').decode('ascii')}")
                except:
                    pass
                raise e

        # Page 1 -> Page 2
        # Note: Page 1 submit button is #submitBtn, next element is input#dob
        # We already have manual retry logic here, but let's standardize if possible. 
        # However, keeping existing logic for Page 1 as it has specific recaptcha handling if needed (though not used in safe_transition)
        # Let's just use safe_transition for Page 2 onwards as requested.

        # Page 2 -> Page 3
        # Click the "Save and Continue" button
        safe_transition("#vehicleInsuranceSubmitBtn", "input#otherPartyFirstName")
        time.sleep(2)

        #Page 3 Other Party Details:
        #First Name
        page.fill("input#otherPartyFirstName", "Johny")
        time.sleep(1)
        #Last Name
        page.fill("input#otherPartyLastName", "Johny")
        time.sleep(1)
        #Phone
        page.fill("#otherPartyPhone", "0412345678")
        time.sleep(1)
        #Insurance Details
        page.click("#isInsuredYes")
        time.sleep(1)
        #Insurer
        page.click("#otherPartyInsurer")
        time.sleep(1)
        page.keyboard.press("ArrowDown")
        time.sleep(0.5)
        page.keyboard.press("Enter")
        time.sleep(1)
        #Claim Number
        page.fill("input#otherPartyPolicyNumber", "222222")
        time.sleep(1)
        #Vehicle Rego State
        page.select_option("#otherPartyRegoState", "NSW")
        time.sleep(1)
        #Vehicle Registration Number
        page.fill("#otherPartyRegistrationNumber", "DK36KT")
        time.sleep(1)
        #Click Check Vehicle:
        page.click("#checkVehicle")
        time.sleep(1)
        #Address
        page.fill("#otherPartyAddress", "SYDNEY, 16 GEMMA GLD, LABRADOR QLD 4215")
        time.sleep(2)
        page.wait_for_selector(".px-3.py-2.cursor-pointer.hover\\:bg-gray-100", timeout=5000)
        page.click(".px-3.py-2.cursor-pointer.hover\\:bg-gray-100")
        time.sleep(3)
        
        # Click and Continue Btn (Page 3 -> Page 4)
        safe_transition("#otherPartySubmitBtn", "#repairsScheduledYes")
        time.sleep(2)

        #Page 4(Additional Information):
        # (Removed manual wait/try block as safe_transition handles it)
        
        page.click("#repairsScheduledYes")
        time.sleep(1)
        #Who is the repairer?
        page.fill("#repairer", "Smash Repair Shop")
        time.sleep(1)
        #What is the repair start date?
        page.fill("#repairStartDate", "12-12-2025")
        time.sleep(1)
        #Do You Require Any Vehicle Accessories or Have Any Special Requirements?
        page.click("#accessoriesOrRequirements")
        page.click("#accessoriesOrRequirementsCheckbox")
        page.keyboard.press("Enter")
        
        # Click the Review and Submit button (Page 4 -> Page 5)
        time.sleep(2)
        safe_transition("#additionalInformationSubmitBtn", "text=Your Claim ID", timeout=30000)
        
        #Page 5(Application Overview):        
        # Click the copy button for Claim ID
        page.click("#claimIdCopyButton")
        # Click Submit My Application button:
        # Page 5 -> Thank You Page
        safe_transition("#submitBtn", "text=Application Submitted", timeout=30000)

        #Thank You Page:
        # Click the Copy button for Claim ID
        page.click("#claimIdCopyButton")
        # Click Know Your Right Button
        page.click("#knowYourRightsButton")
        # Wait for the URL to change to the target "your-rights" page
        page.wait_for_url("https://r2d-au-dev.vercel.app/your-rights", timeout=30000)

        #Your Right:
        page.click("text=How It Works")
        page.click("text=About US")
        page.click("text=FAQ")
        page.click("text=Check Eligibility")
        page.click("text=Articles")

        browser.close()

if __name__ == "__main__":
    run()
