#!/usr/bin/env python3
"""
Analyze census bundles - filter by 'bundle', group by county, find max price per county
"""

import csv
import re

def parse_price(price_str):
    """Convert price string to float"""
    # Remove £ symbol and convert to float
    return float(price_str.replace('£', '').replace(',', ''))

def main():
    # Read the CSV file
    bundles = []
    with open('census_products.csv', 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Filter for bundles only
            if 'bundle' in row['title'].lower():
                bundles.append(row)
    
    # Group by county (first word of title)
    county_prices = {}
    for bundle in bundles:
        # Extract county (first word)
        county = bundle['title'].split()[0]
        price = parse_price(bundle['price'])
        
        # Track maximum price for each county
        if county not in county_prices:
            county_prices[county] = price
        else:
            county_prices[county] = max(county_prices[county], price)
    
    # Display results to console
    print("County Bundle Analysis")
    print("=" * 50)
    print(f"{'County':<30} {'Max Bundle Price':>15}")
    print("-" * 50)
    
    total = 0
    for county, max_price in sorted(county_prices.items()):
        print(f"{county:<30} £{max_price:>14.2f}")
        total += max_price
    
    print("-" * 50)
    print(f"{'Total Counties:':<30} {len(county_prices):>15}")
    print(f"{'Sum of Max Prices:':<30} £{total:>14.2f}")
    
    # Write results to CSV file
    output_file = 'bundle_analysis.csv'
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['county', 'max_bundle_price']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        
        for county, max_price in sorted(county_prices.items()):
            writer.writerow({
                'county': county,
                'max_bundle_price': f'£{max_price:.2f}'
            })
        
        # Add summary rows
        writer.writerow({})  # Empty row
        writer.writerow({'county': 'Total Counties', 'max_bundle_price': str(len(county_prices))})
        writer.writerow({'county': 'Sum of Max Prices', 'max_bundle_price': f'£{total:.2f}'})
    
    print(f"\nResults saved to: {output_file}")

if __name__ == "__main__":
    main()