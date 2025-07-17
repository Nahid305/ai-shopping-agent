# 🤖 AI Shopping Agent

Your intelligent shopping companion that searches across multiple e-commerce platforms to find the best deals!

## ✨ Features

- 🔍 **Smart Search**: Intelligent product search across multiple platforms
- 🛒 **Multi-Platform Support**: Search Flipkart, Amazon, and AJIO simultaneously
- 💰 **Price Comparison**: Find the best deals across different sites
- 🎙️ **Voice Search**: Search using voice commands
- 📱 **Responsive Design**: Works perfectly on desktop and mobile
- 🎨 **Modern UI**: Beautiful, engaging interface similar to real shopping sites
- ⚡ **Fast Performance**: Parallel scraping for quick results
- 🔧 **Advanced Filters**: Filter by price, source, and sort options

## 🚀 Live Demo

Check out the live demo: [AI Shopping Agent](https://ai-shopping-agent.streamlit.app)

## 🛠️ Installation

1. Clone the repository:
```bash
git clone https://github.com/Nahid305/ai-shopping-agent.git
cd ai-shopping-agent
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
streamlit run streamlit_app.py
```

## 📁 Project Structure

```
ai-shopping-agent/
├── streamlit_app.py          # Main Streamlit application
├── components/               # UI components
│   ├── __init__.py
│   └── ui_components.py     # Custom UI components
├── scrapers/                # Web scrapers
│   ├── __init__.py
│   ├── flipkart_scraper.py  # Flipkart scraper
│   ├── amazon_scraper.py    # Amazon scraper
│   └── ajio_scraper.py      # AJIO scraper
├── parser.py                # Query parser
├── utils.py                 # Utility functions
├── requirements.txt         # Dependencies
├── packages.txt             # System packages for cloud
├── .streamlit/config.toml   # Streamlit configuration
├── README.md               # This file
└── .gitignore              # Git ignore file
```

## 🔧 Usage

1. **Text Search**: Enter your search query in the search box
2. **Voice Search**: Click the microphone button to search using voice
3. **Filters**: Use the sidebar to filter by price range, select sources, and sort results
4. **Results**: View products in a beautiful grid layout with images and details

### Example Searches:
- "black headphones under 5000"
- "gaming laptop"
- "wireless bluetooth speaker"
- "running shoes size 9"

## 🛠️ Technical Details

### Dependencies
- `streamlit>=1.28.0` - Web interface framework
- `selenium>=4.15.0` - Web scraping framework
- `webdriver-manager>=4.0.1` - Chrome driver management
- `requests>=2.31.0` - HTTP library
- `beautifulsoup4>=4.12.2` - HTML parsing
- `pyttsx3>=2.90` - Text-to-speech
- `SpeechRecognition>=3.10.0` - Speech-to-text

### Chrome Configuration
The scrapers use headless Chrome optimized for cloud deployment:
- Headless mode for faster scraping
- No-sandbox mode for cloud compatibility
- Disabled GPU for better performance
- Anti-bot detection measures

### Supported Platforms
- **Amazon India** (amazon.in)
- **Flipkart** (flipkart.com)
- **AJIO** (ajio.com)

## 🔧 Troubleshooting

### Common Issues

1. **Chrome Driver Issues**:
   - Chrome browser is automatically managed via webdriver-manager
   - Cloud deployment uses Chromium from packages.txt
   - Fallback scrapers use requests+BeautifulSoup when Selenium fails

2. **Scraping Issues**:
   - Scrapers include multiple fallback selectors for robustness
   - Anti-bot measures help prevent blocking
   - If live scraping fails, sample products are shown for demonstration

3. **Voice Recognition**:
   - Ensure microphone permissions are granted
   - Check internet connection for speech recognition

4. **No Results Found**:
   - This may happen on cloud deployments due to scraping limitations
   - Sample products will be generated for demonstration purposes
   - Try running locally for full scraping functionality

### Performance Tips
- Use specific search terms for better results
- Adjust price ranges to filter results
- Select specific sources if needed

## 🚀 Deployment

### Streamlit Cloud
1. Push your code to GitHub
2. Connect to Streamlit Cloud
3. Use `streamlit_app.py` as the main file
4. Deploy and share your app!

### Local Development
```bash
streamlit run streamlit_app.py
```

Your app will be available at `http://localhost:8501`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Web scraping powered by [Selenium](https://selenium.dev/)
- UI inspired by modern e-commerce platforms

## 📧 Contact

Nahid305 - [GitHub Profile](https://github.com/Nahid305)

Project Link: [https://github.com/Nahid305/ai-shopping-agent](https://github.com/Nahid305/ai-shopping-agent)

---

⭐ **Star this repository if you found it helpful!**
