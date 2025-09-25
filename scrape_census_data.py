#!/usr/bin/env python3
"""
Scrape census data products from britishdataarchive.com and save to CSV
"""

import requests
from bs4 import BeautifulSoup
import csv
import time
import re

def scrape_page(page_num):
    """Scrape a single page of products"""
    url = f"https://britishdataarchive.com/products/?page={page_num}"
    print(f"Scraping page {page_num}...")
    
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching page {page_num}: {e}")
        return None

def parse_products(html_content):
    """Extract product information from HTML"""
    soup = BeautifulSoup(html_content, 'html.parser')
    products = []
    
    # Find the products container (col-md-9)
    products_container = soup.find('div', class_='col-md-9')
    if not products_container:
        return products
    
    # Products are in <a> tags with href to genealogysupplies.com
    product_links = products_container.find_all('a', href=re.compile(r'genealogysupplies\.com/product/'))
    
    for link in product_links:
        product = {}
        
        # Find the title in the first column
        title_div = link.find('div', class_='col-md-10')
        if title_div:
            title_elem = title_div.find('h1')
            if title_elem:
                product['title'] = title_elem.get_text(strip=True)
            
            # Extract description from p tag
            desc_elem = title_div.find('p')
            if desc_elem:
                product['description'] = desc_elem.get_text(strip=True)
        
        # Find the price in the second column
        price_div = link.find('div', class_='col-md-2')
        if price_div:
            price_elem = price_div.find('h1')
            if price_elem:
                product['price'] = price_elem.get_text(strip=True)
        
        if product.get('title'):  # Only add if we have at least a title
            products.append(product)
    
    return products

def main():
    """Main function to scrape all pages and save to CSV"""
    all_products = []
    total_pages = 22
    
    # Scrape all pages
    for page_num in range(1, total_pages + 1):
        html_content = scrape_page(page_num)
        
        if html_content:
            products = parse_products(html_content)
            all_products.extend(products)
            print(f"Found {len(products)} products on page {page_num}")
            
            # Be respectful - add delay between requests
            time.sleep(1)
        else:
            print(f"Skipping page {page_num} due to error")
    
    # Save to CSV
    if all_products:
        csv_filename = 'census_products.csv'
        fieldnames = ['title', 'description', 'price']
        
        with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(all_products)
        
        print(f"\nScraping complete!")
        print(f"Total products found: {len(all_products)}")
        print(f"Data saved to: {csv_filename}")
    else:
        print("No products found")

if __name__ == "__main__":
    main()