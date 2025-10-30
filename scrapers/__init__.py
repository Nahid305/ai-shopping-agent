# Scrapers package for AI Shopping Agent
from .flipkart_scraper import scrape_flipkart
from .amazon_scraper import scrape_amazon
from .ajio_scraper import scrape_ajio

__all__ = ['scrape_flipkart', 'scrape_amazon', 'scrape_ajio']
