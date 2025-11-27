import time
from playwright.sync_api import Page, Locator
import re

class SelfHealingPage:
    def __init__(self, page: Page):
        self.page = page
        self.healed_selectors = {}

    def goto(self, url):
        return self.page.goto(url)

    def wait_for_load_state(self, state="load"):
        return self.page.wait_for_load_state(state)

    def wait_for_selector(self, selector, **kwargs):
        try:
            return self.page.wait_for_selector(selector, **kwargs)
        except Exception:
            print(f"⚠️ Selector failed: {selector}. Attempting to heal...")
            new_selector = self._heal_selector(selector)
            if new_selector:
                print(f"✅ Healed selector: {new_selector}")
                return self.page.wait_for_selector(new_selector, **kwargs)
            raise

    def click(self, selector, **kwargs):
        try:
            # Try original selector
            self.page.click(selector, **kwargs)
        except Exception as e:
            print(f"⚠️ Click failed on: {selector}. Attempting to heal...")
            new_selector = self._heal_selector(selector)
            if new_selector:
                print(f"✅ Healed click using: {new_selector}")
                self.page.click(new_selector, **kwargs)
            else:
                raise e

    def fill(self, selector, value, **kwargs):
        try:
            self.page.fill(selector, value, **kwargs)
        except Exception as e:
            print(f"⚠️ Fill failed on: {selector}. Attempting to heal...")
            new_selector = self._heal_selector(selector)
            if new_selector:
                print(f"✅ Healed fill using: {new_selector}")
                self.page.fill(new_selector, value, **kwargs)
            else:
                raise e

    def query_selector(self, selector):
        el = self.page.query_selector(selector)
        if el:
            return el
        
        print(f"⚠️ Element not found: {selector}. Attempting to heal...")
        new_selector = self._heal_selector(selector)
        if new_selector:
             print(f"✅ Healed query using: {new_selector}")
             return self.page.query_selector(new_selector)
        return None

    def _heal_selector(self, selector):
        """
        Heuristic logic to find an alternative selector.
        """
        import difflib
        
        # 1. Extract potential ID or Name from the selector
        potential_ids = re.findall(r'[#]([\w-]+)', selector)
        potential_names = re.findall(r'\[name=[\'"]?([\w-]+)[\'"]?\]', selector)
        
        keywords = potential_ids + potential_names
        if not keywords and "#" in selector:
            keywords.append(selector.split("#")[-1])
            
        if not keywords:
            # Try to use the whole selector as a keyword if it's simple
            keywords.append(selector.replace("input", "").replace("#", "").replace(".", ""))

        print(f"   [Healing] Keywords extracted: {keywords}")

        # Strategy 1: Exact match on ID/Name (already tried, but good to have)
        for kw in keywords:
            if self.page.is_visible(f"#{kw}"):
                return f"#{kw}"
            if self.page.is_visible(f"[name='{kw}']"):
                return f"[name='{kw}']"

        # Strategy 2: Fuzzy match against all interactive elements on the page
        # This is expensive but effective
        try:
            # Get all inputs and buttons
            elements = self.page.query_selector_all("input, select, textarea, button, a.btn")
            candidates = []
            
            for el in elements:
                try:
                    el_id = el.get_attribute("id") or ""
                    el_name = el.get_attribute("name") or ""
                    el_placeholder = el.get_attribute("placeholder") or ""
                    
                    # Create a signature for this element
                    signature = f"{el_id} {el_name} {el_placeholder}"
                    if signature.strip():
                        candidates.append((el, signature))
                except:
                    continue
            
            # Find best match for each keyword
            for kw in keywords:
                # Get signatures
                signatures = [c[1] for c in candidates]
                # Lower cutoff to 0.2 to be very generous
                matches = difflib.get_close_matches(kw, signatures, n=1, cutoff=0.2)
                
                if matches:
                    best_sig = matches[0]
                    print(f"   [Healing] Found fuzzy match: '{best_sig}' for keyword '{kw}'")
                    # Find the element with this signature
                    for el, sig in candidates:
                        if sig == best_sig:
                            # Construct a selector for this element
                            el_id = el.get_attribute("id")
                            el_name = el.get_attribute("name")
                            
                            if el_id:
                                return f"#{el_id}"
                            if el_name:
                                return f"[name='{el_name}']"
                            
                            # Fallback to placeholder
                            ph = el.get_attribute("placeholder")
                            if ph:
                                return f"[placeholder='{ph}']"
                else:
                    print(f"   [Healing] No fuzzy match found for '{kw}' in {len(signatures)} candidates.")
                    if len(signatures) > 0:
                        print(f"   [Healing] Sample candidates: {signatures[:3]}")
        except Exception as e:
            print(f"   [Healing] Error during fuzzy search: {e}")

        return None

    # Proxy other methods to the underlying page object
    def __getattr__(self, name):
        return getattr(self.page, name)
