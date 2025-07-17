"""
Fallback scrapers using requests + BeautifulSoup for cloud compatibility
These are used when Selenium fails in cloud environments
"""

import requests
from bs4 import BeautifulSoup
import re
import time
import random

def scrape_flipkart_fallback(search_query, budget=None, max_results=15):
    """Fallback Flipkart scraper using requests"""
    print(f"🔄 Using Flipkart fallback scraper for: '{search_query}'...")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1'
    }
    
    try:
        # Create search URL
        search_url = f"https://www.flipkart.com/search?q={search_query.replace(' ', '+')}"
        
        session = requests.Session()
        session.headers.update(headers)
        
        response = session.get(search_url, timeout=10)
        response.raise_for_status()
        
        if response.status_code == 200:
            print(f"✅ Successfully fetched Flipkart page (status: {response.status_code})")
            soup = BeautifulSoup(response.content, 'html.parser')
            
            products = []
            
            # Try multiple selectors for product containers
            product_containers = (
                soup.find_all('div', {'data-id': True}) or
                soup.find_all('div', class_=re.compile(r'.*product.*', re.I)) or
                soup.find_all('div', class_=re.compile(r'.*item.*', re.I))
            )
            
            print(f"📦 Found {len(product_containers)} potential product containers")
            
            for container in product_containers[:max_results]:
                try:
                    # Extract product name
                    name_elem = (
                        container.find('a', class_=re.compile(r'.*title.*', re.I)) or
                        container.find('div', class_=re.compile(r'.*title.*', re.I)) or
                        container.find('span', class_=re.compile(r'.*title.*', re.I)) or
                        container.find('h3') or
                        container.find('h2')
                    )
                    
                    if name_elem:
                        name = name_elem.get_text(strip=True)
                        if len(name) > 10:  # Valid product name
                            # Extract price
                            price_elem = container.find(text=re.compile(r'₹[\d,]+'))
                            if price_elem:
                                price_text = price_elem.strip()
                                price_match = re.search(r'₹([\d,]+)', price_text)
                                if price_match:
                                    price = int(price_match.group(1).replace(',', ''))
                                    
                                    # Extract link
                                    link_elem = container.find('a', href=True)
                                    link = f"https://www.flipkart.com{link_elem['href']}" if link_elem else ""
                                    
                                    # Extract image
                                    img_elem = container.find('img', src=True)
                                    image = img_elem['src'] if img_elem else ""
                                    
                                    products.append({
                                        'title': name,
                                        'price': price,
                                        'link': link,
                                        'image': image,
                                        'source': 'Flipkart'
                                    })
                
                except Exception as e:
                    continue
            
            print(f"✅ Flipkart fallback found {len(products)} products")
            return products
        
        else:
            print(f"❌ Failed to fetch Flipkart page (status: {response.status_code})")
            return []
            
    except Exception as e:
        print(f"❌ Flipkart fallback error: {e}")
        return []

def scrape_amazon_fallback(search_query, budget=None, max_results=15):
    """Fallback Amazon scraper using requests"""
    print(f"🔄 Using Amazon fallback scraper for: '{search_query}'...")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive'
    }
    
    try:
        search_url = f"https://www.amazon.in/s?k={search_query.replace(' ', '+')}"
        
        session = requests.Session()
        session.headers.update(headers)
        
        response = session.get(search_url, timeout=10)
        response.raise_for_status()
        
        if response.status_code == 200:
            print(f"✅ Successfully fetched Amazon page (status: {response.status_code})")
            soup = BeautifulSoup(response.content, 'html.parser')
            
            products = []
            
            # Look for Amazon product containers
            product_containers = soup.find_all('div', {'data-component-type': 's-search-result'})
            
            print(f"📦 Found {len(product_containers)} Amazon product containers")
            
            for container in product_containers[:max_results]:
                try:
                    # Extract product name
                    name_elem = container.find('h2', class_=re.compile(r'.*title.*', re.I))
                    if name_elem:
                        name_link = name_elem.find('a')
                        if name_link:
                            name = name_link.get_text(strip=True)
                            
                            # Extract price
                            price_elem = container.find('span', class_=re.compile(r'.*price.*', re.I))
                            if price_elem:
                                price_text = price_elem.get_text(strip=True)
                                price_match = re.search(r'₹([\d,]+)', price_text)
                                if price_match:
                                    price = int(price_match.group(1).replace(',', ''))
                                    
                                    # Extract link
                                    link = f"https://www.amazon.in{name_link['href']}" if name_link.get('href') else ""
                                    
                                    # Extract image
                                    img_elem = container.find('img', src=True)
                                    image = img_elem['src'] if img_elem else ""
                                    
                                    products.append({
                                        'title': name,
                                        'price': price,
                                        'link': link,
                                        'image': image,
                                        'source': 'Amazon'
                                    })
                
                except Exception as e:
                    continue
            
            print(f"✅ Amazon fallback found {len(products)} products")
            return products
        
        else:
            print(f"❌ Failed to fetch Amazon page (status: {response.status_code})")
            return []
            
    except Exception as e:
        print(f"❌ Amazon fallback error: {e}")
        return []

def generate_sample_products(search_query, budget=None):
    """Generate sample products for demonstration when scrapers fail"""
    print(f"🎭 Generating sample products for: '{search_query}'...")
    
    # Sample product data based on search query
    product_templates = {
        'headphones': [
            {'name': 'Wireless Bluetooth Headphones', 'base_price': 1500},
            {'name': 'Gaming Headset with Mic', 'base_price': 2500},
            {'name': 'Noise Cancelling Earbuds', 'base_price': 3500},
        ],
        'laptop': [
            {'name': 'Gaming Laptop 15.6 inch', 'base_price': 45000},
            {'name': 'Business Laptop Intel i5', 'base_price': 35000},
            {'name': 'Student Laptop AMD Ryzen', 'base_price': 25000},
        ],
        'mobile': [
            {'name': 'Smartphone 6GB RAM 128GB', 'base_price': 15000},
            {'name': 'Android Phone 8GB RAM', 'base_price': 20000},
            {'name': '5G Smartphone Latest Model', 'base_price': 25000},
        ],
        'default': [
            {'name': f'{search_query.title()} - Premium Model', 'base_price': 2000},
            {'name': f'{search_query.title()} - Standard Version', 'base_price': 1500},
            {'name': f'{search_query.title()} - Budget Option', 'base_price': 1000},
        ]
    }
    
    # Determine product category
    query_lower = search_query.lower()
    if 'headphone' in query_lower or 'earphone' in query_lower or 'earbud' in query_lower:
        templates = product_templates['headphones']
    elif 'laptop' in query_lower or 'computer' in query_lower:
        templates = product_templates['laptop']
    elif 'mobile' in query_lower or 'phone' in query_lower or 'smartphone' in query_lower:
        templates = product_templates['mobile']
    else:
        templates = product_templates['default']
    
    products = []
    sources = ['Flipkart', 'Amazon', 'AJIO']
    
    for i, template in enumerate(templates):
        for j, source in enumerate(sources):
            # Add some price variation
            price_variation = random.randint(-500, 500)
            final_price = max(template['base_price'] + price_variation, 500)
            
            # Apply budget filter if specified
            if budget and final_price > budget:
                final_price = int(budget * random.uniform(0.7, 0.95))
            
            products.append({
                'title': f"{template['name']} - {source} Special",
                'price': final_price,
                'link': f"https://example.com/product/{i}{j}",
                'image': "https://via.placeholder.com/200x200?text=Sample+Product",
                'source': source
            })
    
    print(f"✅ Generated {len(products)} sample products")
    return products[:6]  # Return 6 sample products
