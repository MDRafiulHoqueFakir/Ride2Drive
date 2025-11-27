from playwright.sync_api import sync_playwright
import time
import os

def generate_test_script(url, output_file="generated_test.py"):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        print(f"Navigating to {url}...")
        page.goto(url)
        time.sleep(3) # Wait for load

        # Analyze page
        inputs = page.query_selector_all("input, textarea, select")
        buttons = page.query_selector_all("button, a[role='button'], input[type='submit'], a.btn")

        script_lines = [
            "from playwright.sync_api import sync_playwright",
            "from self_healing import SelfHealingPage",
            "import time",
            "",
            "def run():",
            "    print('Starting generated test...')",
            "    with sync_playwright() as p:",
            "        browser = p.chromium.launch(headless=False)",
            "        raw_page = browser.new_page()",
            "        page = SelfHealingPage(raw_page)",
            f"        page.goto('{url}')",
            "        time.sleep(2)",
            ""
        ]

        print(f"Found {len(inputs)} inputs and {len(buttons)} interactive elements.")

        used_names = set()

        for i, inp in enumerate(inputs):
            try:
                tag_name = inp.evaluate("el => el.tagName.toLowerCase()")
                type_attr = inp.get_attribute("type")
                id_attr = inp.get_attribute("id")
                name_attr = inp.get_attribute("name")
                placeholder = inp.get_attribute("placeholder")
                
                if type_attr == "hidden":
                    continue

                selector = ""
                if id_attr:
                    selector = f"#{id_attr}"
                elif name_attr:
                    selector = f"[name='{name_attr}']"
                elif placeholder:
                    selector = f"[placeholder='{placeholder}']"
                else:
                    continue # Skip hard-to-select inputs for now

                if selector in used_names:
                    continue
                used_names.add(selector)

                if tag_name == "select":
                    script_lines.append(f"        # Select option in {selector}")
                    script_lines.append(f"        try: page.select_option(\"{selector}\", index=1)")
                    script_lines.append(f"        except: pass")
                elif type_attr in ["checkbox", "radio"]:
                    script_lines.append(f"        # Check {selector}")
                    script_lines.append(f"        page.check(\"{selector}\")")
                else:
                    script_lines.append(f"        # Fill {selector}")
                    script_lines.append(f"        page.fill(\"{selector}\", \"test_value\")")
                
                script_lines.append("        time.sleep(0.5)")

            except Exception as e:
                print(f"Error processing input {i}: {e}")

        # Add a comment for buttons but don't click them all automatically to avoid navigating away immediately
        script_lines.append("")
        script_lines.append("        # Potential buttons to click (uncomment to use):")
        for btn in buttons:
            try:
                text = btn.inner_text().strip()
                if not text:
                    continue
                # Clean text for comment
                clean_text = text.replace('\n', ' ')
                script_lines.append(f"        # page.click(\"text={clean_text}\")")
            except:
                pass

        script_lines.append("")
        script_lines.append("        browser.close()")
        script_lines.append("")
        script_lines.append("if __name__ == '__main__':")
        script_lines.append("    run()")

        print("DEBUG: First 20 lines of generated script:")
        for line in script_lines[:20]:
            print(repr(line))

        with open(output_file, "w", encoding="utf-8") as f:
            f.write("\n".join(script_lines))
            f.flush()
            os.fsync(f.fileno())
        
        print(f"Generated test script saved to {output_file}")
        browser.close()

if __name__ == "__main__":
    # Default to the Ride2Drive URL if run directly
    target_url = "https://r2d-au-dev.vercel.app/"
    generate_test_script(target_url, "generated_ride2drive_test.py")
