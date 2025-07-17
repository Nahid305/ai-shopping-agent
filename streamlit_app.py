import streamlit as st
from components.ui_components import (
    apply_custom_css, 
    create_hero_section, 
    create_search_section,
    create_filters_section,
    create_product_card,
    create_footer
)
from scrapers.flipkart_scraper import scrape_flipkart
from scrapers.amazon_scraper import scrape_amazon
from scrapers.ajio_scraper import scrape_ajio
from scrapers.fallback_scrapers import scrape_flipkart_fallback, scrape_amazon_fallback, generate_sample_products
from parser import parse_query
from utils import filter_by_budget, shorten_title, listen
import time
import random

# --- Page Configuration ---
st.set_page_config(
    page_title="🛍️ AI Shopping Agent - Your Smart Shopping Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/yourusername/ai-shopping-agent',
        'Report a bug': 'https://github.com/yourusername/ai-shopping-agent/issues',
        'About': "# AI Shopping Agent\nYour intelligent shopping companion that searches across multiple platforms!"
    }
)

# Apply custom CSS
apply_custom_css()

# --- State Management ---
if 'query' not in st.session_state:
    st.session_state.query = ""
if 'search_results' not in st.session_state:
    st.session_state.search_results = []
if 'search_executed' not in st.session_state:
    st.session_state.search_executed = False
if 'selected_sources' not in st.session_state:
    st.session_state.selected_sources = ['Flipkart', 'Amazon', 'AJIO']
if 'price_range' not in st.session_state:
    st.session_state.price_range = (0, 100000)
if 'sort_by' not in st.session_state:
    st.session_state.sort_by = 'Relevance'

# --- Helper Functions ---
def reset_search():
    """Reset search state for new query"""
    st.session_state.search_results = []
    st.session_state.search_executed = False

def perform_search(query, sources, budget):
    """Perform search across selected sources with fallback options"""
    parsed = parse_query(query)
    all_results = []
    search_text = f"{parsed.get('color', '')} {parsed['product']}".strip()
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    total_sources = len(sources)
    progress_step = 1.0 / total_sources if total_sources > 0 else 1.0
    
    try:
        if 'Flipkart' in sources:
            status_text.text("🔍 Searching Flipkart...")
            progress_bar.progress(0.1)
            try:
                flipkart_results = scrape_flipkart(search_text, budget)
                if not flipkart_results:  # If no results, try fallback
                    status_text.text("🔄 Trying Flipkart fallback method...")
                    flipkart_results = scrape_flipkart_fallback(search_text, budget)
                all_results.extend(flipkart_results)
                print(f"Flipkart results: {len(flipkart_results)}")
            except Exception as e:
                print(f"Flipkart error: {e}")
                status_text.text("🔄 Using Flipkart fallback...")
                try:
                    flipkart_results = scrape_flipkart_fallback(search_text, budget)
                    all_results.extend(flipkart_results)
                except Exception as e2:
                    print(f"Flipkart fallback error: {e2}")
            progress_bar.progress(progress_step)
            time.sleep(0.5)
        
        if 'Amazon' in sources:
            status_text.text("🔍 Searching Amazon...")
            progress_bar.progress(0.1 + progress_step)
            try:
                amazon_results = scrape_amazon(search_text, budget)
                if not amazon_results:  # If no results, try fallback
                    status_text.text("🔄 Trying Amazon fallback method...")
                    amazon_results = scrape_amazon_fallback(search_text, budget)
                all_results.extend(amazon_results)
                print(f"Amazon results: {len(amazon_results)}")
            except Exception as e:
                print(f"Amazon error: {e}")
                status_text.text("🔄 Using Amazon fallback...")
                try:
                    amazon_results = scrape_amazon_fallback(search_text, budget)
                    all_results.extend(amazon_results)
                except Exception as e2:
                    print(f"Amazon fallback error: {e2}")
            progress_bar.progress(2 * progress_step)
            time.sleep(0.5)
        
        if 'AJIO' in sources:
            status_text.text("🔍 Searching AJIO...")
            progress_bar.progress(0.1 + 2 * progress_step)
            try:
                ajio_results = scrape_ajio(search_text, budget)
                all_results.extend(ajio_results)
                print(f"AJIO results: {len(ajio_results)}")
            except Exception as e:
                print(f"AJIO error: {e}")
            progress_bar.progress(1.0)
            time.sleep(0.5)
        
        # If no results from any scraper, generate sample products for demo
        if not all_results:
            status_text.text("🎭 Generating sample results for demonstration...")
            sample_results = generate_sample_products(search_text, budget)
            all_results.extend(sample_results)
            progress_bar.progress(1.0)
            time.sleep(1)
        
        status_text.text("✅ Search completed!")
        time.sleep(1)
        progress_bar.empty()
        status_text.empty()
        
    except Exception as e:
        st.error(f"Search error: {str(e)}")
        progress_bar.empty()
        status_text.empty()
    
    return filter_by_budget(all_results, budget)

def sort_results(results, sort_by):
    """Sort results based on selected criteria"""
    if sort_by == 'Price: Low to High':
        return sorted(results, key=lambda x: x.get('price', 0))
    elif sort_by == 'Price: High to Low':
        return sorted(results, key=lambda x: x.get('price', 0), reverse=True)
    elif sort_by == 'Source':
        return sorted(results, key=lambda x: x.get('source', ''))
    else:  # Relevance
        return results

# --- Main App ---
def main():
    # Hero Section
    create_hero_section()
    
    # Search Section
    with st.container():
        col1, col2 = st.columns([3, 1])
        
        with col1:
            search_query, search_button_clicked = create_search_section()
            if search_query != st.session_state.query:
                st.session_state.query = search_query
                reset_search()
        
        with col2:
            # Voice Search Button
            if st.button("🎙️ Voice Search", key="voice_search", help="Click to search with voice"):
                with st.spinner("🎧 Listening..."):
                    voice_text = listen()
                    if voice_text:
                        st.session_state.query = voice_text
                        reset_search()
                        st.rerun()
    
    # Handle main search button click
    if search_button_clicked:
        # Get current filter values from sidebar
        sources = st.session_state.selected_sources
        price_range = st.session_state.price_range
        
        if not st.session_state.query.strip():
            st.warning("⚠️ Please enter a search query")
        elif not sources:
            st.warning("⚠️ Please select at least one shopping site in the sidebar")
        else:
            st.session_state.search_executed = True
            with st.spinner("🔍 Searching across platforms..."):
                results = perform_search(
                    st.session_state.query,
                    sources,
                    price_range[1]
                )
                st.session_state.search_results = results
                st.rerun()
    
    # Filters Section
    with st.sidebar:
        st.markdown("## 🎛️ Filters & Options")
        
        # Source Selection
        sources = st.multiselect(
            "🛒 Select Shopping Sites:",
            ['Flipkart', 'Amazon', 'AJIO'],
            default=st.session_state.selected_sources,
            help="Choose which shopping sites to search"
        )
        st.session_state.selected_sources = sources
        
        # Price Range
        price_range = st.slider(
            "💰 Price Range (₹):",
            min_value=0,
            max_value=100000,
            value=st.session_state.price_range,
            step=1000,
            help="Set your budget range"
        )
        st.session_state.price_range = price_range
        
        # Sort Options
        sort_option = st.selectbox(
            "📊 Sort by:",
            ['Relevance', 'Price: Low to High', 'Price: High to Low', 'Source'],
            index=['Relevance', 'Price: Low to High', 'Price: High to Low', 'Source'].index(st.session_state.sort_by)
        )
        st.session_state.sort_by = sort_option
        
        # Search Button
        search_disabled = not st.session_state.query.strip() or not sources
        
        if st.button(
            "🔍 Search Products", 
            disabled=search_disabled,
            key="sidebar_search",
            help="Start searching across selected platforms"
        ):
            if not st.session_state.query.strip():
                st.warning("⚠️ Please enter a search query")
            elif not sources:
                st.warning("⚠️ Please select at least one shopping site")
            else:
                st.session_state.search_executed = True
                with st.spinner("🔍 Searching across platforms..."):
                    results = perform_search(
                        st.session_state.query,
                        sources,
                        price_range[1]
                    )
                    st.session_state.search_results = results
                    st.rerun()
    
    # Results Section
    if st.session_state.search_executed:
        st.markdown("---")
        
        # Debug information
        st.info(f"🔍 Search executed for: '{st.session_state.query}' | Found: {len(st.session_state.search_results)} products")
        
        # Results Header
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            st.markdown("## 🛍️ Search Results")
        
        with col2:
            if st.session_state.search_results:
                st.metric("Found Products", len(st.session_state.search_results))
        
        with col3:
            if st.button("🔄 New Search", key="new_search"):
                reset_search()
                st.session_state.query = ""
                st.rerun()
        
        # Display Results
        if st.session_state.search_results:
            sorted_results = sort_results(st.session_state.search_results, st.session_state.sort_by)
            
            # Filter by price range
            filtered_results = [
                item for item in sorted_results 
                if price_range[0] <= item.get('price', 0) <= price_range[1]
            ]
            
            # Debug: Show filtering details
            st.write(f"📊 Total results: {len(st.session_state.search_results)} | After sorting: {len(sorted_results)} | After price filter: {len(filtered_results)}")
            st.write(f"💰 Price range filter: ₹{price_range[0]:,} - ₹{price_range[1]:,}")
            
            if filtered_results:
                st.success(f"✅ Found {len(filtered_results)} products matching your criteria")
                
                # Display products in grid
                cols_per_row = 3
                for i in range(0, len(filtered_results), cols_per_row):
                    cols = st.columns(cols_per_row)
                    for j in range(cols_per_row):
                        if i + j < len(filtered_results):
                            with cols[j]:
                                create_product_card(filtered_results[i + j])
            else:
                st.warning("🔍 No products found in your price range. Try adjusting the filters.")
                # Show some sample prices to help debug
                if sorted_results:
                    sample_prices = [item.get('price', 0) for item in sorted_results[:5]]
                    st.write(f"Sample product prices: {sample_prices}")
        else:
            st.info("🔍 No products found. Try different search terms or check if the sites are accessible.")
    
    # Footer
    create_footer()

if __name__ == "__main__":
    main()
