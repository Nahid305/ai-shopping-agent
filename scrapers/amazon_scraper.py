# amazon_scraper.py
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
import time
import re

def scrape_amazon(query, budget=None, max_results=15): # Reduced from 30 to 15 for faster results
    print(f"🤖 Starting Amazon scrape for: '{query}'...")

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--disable-features=VizDisplayCompositor")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--log-level=3")
    driver = webdriver.Chrome(options=options)
    driver.get(f"https://www.amazon.in/s?k={query.replace(' ', '+')}")

    time.sleep(2)  # Reduced from 3 to 2 seconds

    blocks = driver.find_elements(By.XPATH, "//div[@data-component-type='s-search-result']")
    print(f"📦 Found {len(blocks)} potential blocks.")
    
    products = []

    for block in blocks[:max_results]:
        try:
            # Try multiple selectors for product name
            name = None
            name_selectors = ['h2 a span', 'h2 span', 'h2', '.s-title-instructions-style h2', '.s-link-style h2']
            
            for selector in name_selectors:
                try:
                    name_element = block.find_element(By.CSS_SELECTOR, selector)
                    name = name_element.text.strip()
                    if name:
                        break
                except NoSuchElementException:
                    continue
            
            if not name:
                continue
            
            # Find price element - Try multiple selectors
            price = None
            price_selectors = [
                '.a-price-whole', '.a-price .a-offscreen', '.a-price-range .a-price .a-offscreen',
                '.a-price-symbol + .a-price-whole', '.a-price-fraction'
            ]
            
            for selector in price_selectors:
                try:
                    price_element = block.find_element(By.CSS_SELECTOR, selector)
                    price_text = price_element.text or price_element.get_attribute('textContent')
                    price_match = re.search(r'[\d,]+', price_text)
                    if price_match:
                        price = int(price_match.group(0).replace(",", ""))
                        break
                except NoSuchElementException:
                    continue
            
            if price is None:
                continue

            # Get product link
            link = None
            try:
                link_element = block.find_element(By.TAG_NAME, 'a')
                link = link_element.get_attribute('href')
                if link and not link.startswith('http'):
                    link = 'https://www.amazon.in' + link
            except NoSuchElementException:
                continue

            # Get product image
            image_url = None
            image_selectors = [
                'img.s-image', 'img[data-image-latency]', 'img[src*="images-amazon"]',
                '.s-image img', 'img.a-dynamic-image', 'img[alt*="' + name[:20] + '"]'
            ]
            
            for selector in image_selectors:
                try:
                    img_element = block.find_element(By.CSS_SELECTOR, selector)
                    image_url = img_element.get_attribute('src')
                    if image_url and ('images-amazon' in image_url or 'ssl-images-amazon' in image_url):
                        break
                except NoSuchElementException:
                    continue
            
            # Fallback to data-src if src is not found
            if not image_url:
                for selector in image_selectors:
                    try:
                        img_element = block.find_element(By.CSS_SELECTOR, selector)
                        image_url = img_element.get_attribute('data-src')
                        if image_url and ('images-amazon' in image_url or 'ssl-images-amazon' in image_url):
                            break
                    except NoSuchElementException:
                        continue

            if name and price is not None and link:
                products.append({
                    "title": name,
                    "price": price,
                    "link": link,
                    "image": image_url,
                    "source": "Amazon"
                })
        except Exception as e:
            print(f"❌ [Amazon] An unexpected error occurred while processing a block: {e}")
            continue

    driver.quit()
    return products