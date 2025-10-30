from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import time
import re

def scrape_ajio(query, budget):
    print(f"🤖 Starting AJIO scrape for: '{query}'...")
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-features=VizDisplayCompositor")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    options.add_argument("--log-level=3")
    driver = webdriver.Chrome(options=options)

    results = []
    try:
        search_query = query.replace(" ", "%20")
        url = f"https://www.ajio.com/search/?text={search_query}"
        driver.get(url)
        time.sleep(3)  # Reduced from 8 to 3 seconds

        # Reduced scroll iterations from 5 to 3
        for _ in range(3):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)  # Reduced from 3 to 1 second

        # Try multiple selectors for product containers
        container_selectors = [
            '.item', 'div.item', '[data-testid="plp-item"]', 
            '.rilrtl-products-list__item', '.product-item', '.product',
            '.items', '.product-base', '.product-tuple', '.fnl-plp-item',
            '.product-tile', '.product-card'
        ]
        
        items = []
        for selector in container_selectors:
            try:
                items = driver.find_elements(By.CSS_SELECTOR, selector)
                if items:
                    print(f"📦 Found {len(items)} items with selector: {selector}")
                    break
            except:
                continue
        
        if not items:
            print("📦 Found 0 potential blocks on AJIO.")
            return results

        for item in items[:15]:  # Reduced from 30 to 15 for faster results
            try:
                name = None
                # Try multiple selectors for product names
                name_selectors = [
                    '.nameCls', '.name', '.product-name', '.itemname', 
                    '[data-testid="product-name"]', '.product-title',
                    '.brand', '.fnl-plp-title', '.product-base',
                    '.fnl-plp-title-link', '.product-link'
                ]
                
                for selector in name_selectors:
                    try:
                        name_element = item.find_element(By.CSS_SELECTOR, selector)
                        name = name_element.text.strip()
                        if name and len(name) > 5:
                            break
                    except NoSuchElementException:
                        continue
                
                if not name:
                    continue
                
                price = None
                # Try multiple selectors for price
                price_selectors = [
                    '.price', '.price-current', '.final-price', 
                    '[data-testid="price"]', '.priceContainer',
                    '.fnl-plp-price', '.price-block', '.price-value',
                    '.price-current-value', '.final-price-value'
                ]
                
                for selector in price_selectors:
                    try:
                        price_element = item.find_element(By.CSS_SELECTOR, selector)
                        price_text = price_element.text.strip()
                        price_match = re.search(r'[\d,]+', price_text)
                        if price_match:
                            price = int(price_match.group(0).replace(",", ""))
                            break
                    except NoSuchElementException:
                        continue
                
                if price is None:
                    continue

                link = None
                # Try to get link from anchor tags
                try:
                    link_element = item.find_element(By.TAG_NAME, 'a')
                    link = link_element.get_attribute('href')
                    
                    # Prepend base URL if link is relative
                    if link and not link.startswith("http"):
                        link = "https://www.ajio.com" + link
                except NoSuchElementException:
                    continue

                # Get product image
                image_url = None
                image_selectors = [
                    'img.rilrtl-lazy-img', 'img[data-src*="ajio"]', 'img[src*="ajio"]',
                    'img.fnl-plp-img', 'img.product-image', 'img'
                ]
                
                for selector in image_selectors:
                    try:
                        img_element = item.find_element(By.CSS_SELECTOR, selector)
                        image_url = img_element.get_attribute('src') or img_element.get_attribute('data-src')
                        if image_url and ('ajio' in image_url or 'assets' in image_url):
                            break
                    except NoSuchElementException:
                        continue

                if name and price is not None and link:
                    results.append({
                        "title": name,
                        "price": price,
                        "link": link,
                        "image": image_url,
                        "source": "AJIO"
                    })
            except Exception as e:
                print(f"❌ [AJIO] An unexpected error occurred while processing an item: {e}")
                continue

    except Exception as e:
        print(f"❌ [AJIO] Error during scraping: {e}")
    finally:
        print(f"✅ AJIO scrape complete. Found {len(results)} products.")
        driver.quit()

    return results
