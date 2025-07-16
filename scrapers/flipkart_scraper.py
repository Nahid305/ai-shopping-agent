import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time


def scrape_flipkart(search_query, budget=None):
    print(f"🤖 Starting Flipkart scrape for: '{search_query}'...")

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-features=VizDisplayCompositor")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--log-level=3")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    
    try:
        # Go directly to search results page
        search_url = f"https://www.flipkart.com/search?q={search_query.replace(' ', '%20')}"
        driver.get(search_url)
        time.sleep(2)  # Reduced from 5 to 2 seconds

        # Wait for product grid with multiple possible selectors
        try:
            WebDriverWait(driver, 15).until(
                EC.any_of(
                    EC.presence_of_element_located((By.XPATH, "//div[@data-id]")),
                    EC.presence_of_element_located((By.CSS_SELECTOR, "[data-id]")),
                    EC.presence_of_element_located((By.CSS_SELECTOR, ".KzDlHZ")),
                    EC.presence_of_element_located((By.CSS_SELECTOR, "._2WkVRV")),
                    EC.presence_of_element_located((By.CSS_SELECTOR, ".s1Q9rs")),
                    EC.presence_of_element_located((By.CSS_SELECTOR, ".CGtC98"))
                )
            )
            print("✅ Products loaded.")
        except TimeoutException:
            print("❌ No products found on Flipkart for this query.")
            return []

        products = []
        
        # Try different selectors for product containers
        blocks = driver.find_elements(By.XPATH, "//div[@data-id]")
        if not blocks:
            blocks = driver.find_elements(By.CSS_SELECTOR, "[data-id]")
        if not blocks:
            blocks = driver.find_elements(By.CSS_SELECTOR, ".CGtC98")
        if not blocks:
            # Try looking for product cards in a different way
            blocks = driver.find_elements(By.CSS_SELECTOR, "div[data-testid='product-card']")
        if not blocks:
            blocks = driver.find_elements(By.CSS_SELECTOR, ".s1Q9rs")
        
        print(f"📦 Found {len(blocks)} potential blocks on Flipkart.")

        for i, block in enumerate(blocks[:15]):  # Reduced from 30 to 15 for faster results
            try:
                name = None
                # Try multiple selectors for product names
                name_selectors = [
                    ".KzDlHZ", "._2WkVRV", ".s1Q9rs", "a.s1Q9rs", 
                    "div._4rR01T", "a.IRpwCc", "._4rR01T", ".IRpwCc", 
                    "a[target='_blank']", ".wjcEIp", "div.col-7-12 a",
                    "h2", "a span", ".B_NuCI", "._2cLu-l"
                ]
                
                for selector in name_selectors:
                    try:
                        name_element = block.find_element(By.CSS_SELECTOR, selector)
                        name = name_element.get_attribute("textContent") or name_element.text
                        if name and name.strip():
                            name = name.strip()
                            # Skip if it's just a generic element
                            if len(name) > 5 and not name.lower().startswith('http'):
                                break
                    except NoSuchElementException:
                        continue
                
                if not name or len(name) < 5:
                    continue

                price = None
                # Try multiple selectors for price
                price_selectors = [
                    ".Nx9bqj", "._1_WHN1", ".yRaY8j", "._25b18c",
                    "div._30jeq3", "div._2rQ-ZK", "._30jeq3", "._2rQ-ZK",
                    "._1p_IlO", ".yhZ8ez", ".y6uJxm", "._3auQ3N"
                ]
                
                for selector in price_selectors:
                    try:
                        price_element = block.find_element(By.CSS_SELECTOR, selector)
                        price_text = price_element.text.strip()
                        price_match = re.search(r"₹\s*([\d,]+)", price_text)
                        if price_match:
                            price_str = price_match.group(1).replace(",", "")
                            price = int(price_str)
                            break
                    except (NoSuchElementException, ValueError):
                        continue
                
                if price is None:
                    continue

                link = None
                # Try to get link from anchor tags
                try:
                    link_element = block.find_element(By.TAG_NAME, "a")
                    href = link_element.get_attribute("href")
                    if href and ("flipkart.com" in href or href.startswith("/")):
                        link = href if href.startswith("http") else f"https://www.flipkart.com{href}"
                except NoSuchElementException:
                    continue
                
                if not link:
                    continue

                # Get product image
                image_url = None
                image_selectors = [
                    'img._396cs4', 'img._2r_T1I', 'img.q6DClP', 'img._53J4C-',
                    'img[src*="flipkart"]', 'img[alt*="' + name[:20] + '"]', 'img'
                ]
                
                for selector in image_selectors:
                    try:
                        img_element = block.find_element(By.CSS_SELECTOR, selector)
                        image_url = img_element.get_attribute('src')
                        if image_url and ('flipkart' in image_url or 'rukminim' in image_url):
                            break
                    except NoSuchElementException:
                        continue
                
                # Fallback to data-src
                if not image_url:
                    for selector in image_selectors:
                        try:
                            img_element = block.find_element(By.CSS_SELECTOR, selector)
                            image_url = img_element.get_attribute('data-src')
                            if image_url and ('flipkart' in image_url or 'rukminim' in image_url):
                                break
                        except NoSuchElementException:
                            continue
                
                # All details found, append to list
                products.append({
                    "title": name,
                    "price": price,
                    "link": link,
                    "image": image_url,
                    "source": "Flipkart"
                })

            except Exception as e:
                print(f"❌ [Flipkart] An unexpected error occurred while processing a block: {e}")
                continue

        print(f"✅ Flipkart scrape complete. Found {len(products)} products.")
        return products
        
    except Exception as e:
        print(f"❌ [Flipkart] Error during scraping: {e}")
        return []
    finally:
        driver.quit()
