import streamlit as st
import base64
from typing import Dict, Any

def apply_custom_css():
    """Apply custom CSS for enhanced UI"""
    st.markdown("""
    <style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
    
    /* Global Styles */
    .stApp {
        font-family: 'Poppins', sans-serif;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    /* Hero Section */
    .hero-container {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 3rem 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    }
    
    .hero-title {
        font-size: 3.5rem;
        font-weight: 700;
        color: white;
        margin-bottom: 1rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .hero-subtitle {
        font-size: 1.3rem;
        color: #f8f9fa;
        margin-bottom: 2rem;
        font-weight: 300;
    }
    
    .hero-features {
        display: flex;
        justify-content: center;
        gap: 2rem;
        flex-wrap: wrap;
        margin-top: 2rem;
    }
    
    .feature-item {
        background: rgba(255,255,255,0.1);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        min-width: 150px;
        backdrop-filter: blur(10px);
    }
    
    /* Search Section */
    .search-container {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        margin-bottom: 2rem;
    }
    
    /* Search Button Styling */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        font-weight: 600;
        transition: all 0.3s ease;
        height: 3rem;
    }
    
    .stButton > button[kind="primary"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    
    /* Product Cards */
    .product-card {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        border: 1px solid #e9ecef;
    }
    
    .product-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 30px rgba(0,0,0,0.15);
    }
    
    .product-image {
        width: 100%;
        height: 200px;
        object-fit: cover;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    
    .product-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #2c3e50;
        margin-bottom: 0.5rem;
        line-height: 1.4;
    }
    
    .product-price {
        font-size: 1.5rem;
        font-weight: 700;
        color: #27ae60;
        margin-bottom: 0.5rem;
    }
    
    .product-source {
        display: inline-block;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 500;
        margin-bottom: 1rem;
    }
    
    .source-flipkart {
        background: #ff6b35;
        color: white;
    }
    
    .source-amazon {
        background: #ff9900;
        color: white;
    }
    
    .source-ajio {
        background: #c70039;
        color: white;
    }
    
    .product-link {
        display: inline-block;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 0.8rem 1.5rem;
        border-radius: 25px;
        text-decoration: none;
        font-weight: 500;
        transition: all 0.3s ease;
        text-align: center;
        width: 100%;
    }
    
    .product-link:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        text-decoration: none;
        color: white;
    }
    
    /* Sidebar Styles */
    .sidebar .sidebar-content {
        background: white;
        border-radius: 15px;
        padding: 1rem;
    }
    
    /* Button Styles */
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.8rem 2rem;
        font-weight: 500;
        transition: all 0.3s ease;
        width: 100%;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
    
    /* Footer */
    .footer {
        background: #2c3e50;
        color: white;
        padding: 2rem;
        border-radius: 15px;
        margin-top: 3rem;
        text-align: center;
    }
    
    .footer-links {
        display: flex;
        justify-content: center;
        gap: 2rem;
        margin-bottom: 1rem;
    }
    
    .footer-links a {
        color: #ecf0f1;
        text-decoration: none;
        transition: color 0.3s ease;
    }
    
    .footer-links a:hover {
        color: #3498db;
    }
    
    /* Responsive Design */
    @media (max-width: 768px) {
        .hero-title {
            font-size: 2.5rem;
        }
        
        .hero-features {
            flex-direction: column;
            align-items: center;
        }
        
        .product-card {
            margin-bottom: 1rem;
        }
    }
    
    /* Loading Animation */
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.5; }
        100% { opacity: 1; }
    }
    
    .loading {
        animation: pulse 1.5s infinite;
    }
    
    /* Custom Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #f1f1f1;
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #5a6fd8 0%, #6a4190 100%);
    }
    </style>
    """, unsafe_allow_html=True)

def create_hero_section():
    """Create the hero section with branding and features"""
    st.markdown("""
    <div class="hero-container">
        <h1 class="hero-title">🤖 AI Shopping Agent</h1>
        <p class="hero-subtitle">Your Intelligent Shopping Companion - Search Across Multiple Platforms Instantly</p>
        <div class="hero-features">
            <div class="feature-item">
                <h3>🔍</h3>
                <p>Smart Search</p>
            </div>
            <div class="feature-item">
                <h3>💰</h3>
                <p>Best Prices</p>
            </div>
            <div class="feature-item">
                <h3>🛒</h3>
                <p>Multiple Sites</p>
            </div>
            <div class="feature-item">
                <h3>🎙️</h3>
                <p>Voice Search</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def create_search_section():
    """Create the main search input section with search button"""
    st.markdown('<div class="search-container">', unsafe_allow_html=True)
    
    # Search input with button in the same row
    col1, col2 = st.columns([4, 1])
    
    with col1:
        query = st.text_input(
            "Search Products",
            placeholder="🔍 Search for products... (e.g., 'black headphones under 5000')",
            value=st.session_state.get('query', ''),
            key="search_input",
            help="Enter product name, color, brand, or any specific requirements",
            label_visibility="hidden"
        )
    
    with col2:
        search_clicked = st.button("🔍 Search", key="main_search_button", type="primary", use_container_width=True)
    
    # Quick search suggestions
    st.markdown("**💡 Quick Suggestions:**")
    suggestions = [
        "wireless headphones", "gaming laptop", "smartphone under 20000", 
        "running shoes", "bluetooth speaker", "smartwatch"
    ]
    
    cols = st.columns(len(suggestions))
    for i, suggestion in enumerate(suggestions):
        with cols[i]:
            if st.button(f"🔍 {suggestion}", key=f"suggestion_{i}"):
                st.session_state.query = suggestion
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    return query, search_clicked

def create_filters_section():
    """Create the filters section in sidebar"""
    pass  # This is handled in the main app

def create_product_card(product: Dict[str, Any]):
    """Create an enhanced product card"""
    if not all(key in product for key in ['title', 'price', 'source', 'link']):
        return
    
    # Source-specific styling
    source_class = f"source-{product['source'].lower()}"
    
    # Card HTML
    card_html = f"""
    <div class="product-card">
        <div style="text-align: center;">
    """
    
    # Product image
    if product.get('image'):
        card_html += f'<img src="{product["image"]}" class="product-image" alt="{product["title"]}" onerror="this.src=\'https://via.placeholder.com/200x200?text=No+Image\'">'
    else:
        card_html += '<img src="https://via.placeholder.com/200x200?text=No+Image" class="product-image" alt="No Image">'
    
    # Product details
    card_html += f"""
        </div>
        <div class="product-title">{product['title'][:100]}{'...' if len(product['title']) > 100 else ''}</div>
        <div class="product-price">₹{product['price']:,}</div>
        <span class="product-source {source_class}">{product['source']}</span>
        <br><br>
        <a href="{product['link']}" target="_blank" class="product-link">
            🛒 View Product
        </a>
    </div>
    """
    
    st.markdown(card_html, unsafe_allow_html=True)

def create_footer():
    """Create the footer section"""
    st.markdown("""
    <div class="footer">
        <div class="footer-links">
            <a href="https://github.com/yourusername/ai-shopping-agent" target="_blank">📁 GitHub</a>
            <a href="https://github.com/yourusername/ai-shopping-agent/issues" target="_blank">🐛 Report Bug</a>
            <a href="mailto:your.email@example.com">📧 Contact</a>
        </div>
        <p>© 2025 AI Shopping Agent. Built with ❤️ using Streamlit</p>
        <p>🔍 Powered by intelligent web scraping across Flipkart, Amazon & AJIO</p>
    </div>
    """, unsafe_allow_html=True)

def show_loading_animation():
    """Show loading animation during search"""
    st.markdown("""
    <div style="text-align: center; padding: 2rem;">
        <div class="loading">
            <h2>🔍 Searching across platforms...</h2>
            <p>Please wait while we fetch the best deals for you!</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
