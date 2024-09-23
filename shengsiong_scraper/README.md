# Sheng Siong Web Scraper

This project is a web scraper for Sheng Siong's online store, built using Scrapy and Selenium. It extracts product information from the search results page for "your_search_query" products. The default search was conducted on 'nuts'.

## Features

- Scrapes product details including name, weight, pricing, origin, dietary information, and image URL
- Handles both regular and promotional pricing
- Uses Selenium to interact with dynamic content and load more products
- Extracts data from modal popups for detailed product information

## Setup

1. Install required packages:
   ```
   pip install scrapy selenium webdriver_manager
   ```

2. Ensure you have Chrome browser installed.

3. The script uses WebDriver Manager, so you don't need to manually download ChromeDriver.

## Usage

1. Navigate to the project directory.

2. Run the spider:
   ```
   scrapy crawl shengsiongspider -o output.json
   ```
   This will start the scraper and save the results in `output.json`.

## How it Works

1. The spider starts at the search URL for "your_search_query" products.

2. It uses Selenium to scroll through the page, loading all products.

3. For each product:
   - It clicks on the product to open a modal with detailed information.
   - Extracts the required data from the modal.
   - Closes the modal before moving to the next product.

4. The extracted data is yielded as a dictionary for each product.

## Data Extracted

- Product name
- Weight/UOM
- Normal price
- Discounted price (if applicable)
- Origin
- Dietary information
- Image URL

## Notes

- The scraper uses a `scroll_to_bottom` method to ensure all products are loaded before extraction begins.
- It handles both regular pricing and promotional pricing scenarios.
- The scraper closes the Selenium WebDriver when finished to free up resources.

## Customization

You can modify the `start_urls` in the spider class to scrape different product categories or search terms.

## Disclaimer

This scraper is for educational purposes only. Always respect the website's robots.txt file and terms of service when scraping.
