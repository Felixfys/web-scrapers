# Fairprice Product Web Scraper

This project is a web scraper built with Scrapy to collect product SKU data from the Fairprice supermarket website API. It focuses on extracting detailed product information from search results and uses ScrapOps for managing user agents and proxies.

## Project Overview

The scraper is designed to:
- Fetch product data from Fairprice's website API
- Handle pagination to collect data across multiple pages
- Parse JSON responses to extract relevant product information
- Use ScrapOps for rotating user agents and proxies to improve scraping reliability
- Store the collected data in a structured format

## How it Works

- Fairprice uses an AJAX-based API for simulating infinite scrolling on their product search page.
- The API endpoint it uses: `https://website-api.omni.fairprice.com.sg/api/product/...`
  - query={search_term}
  - page={page_number}
  - sort={sort_option}
  - filter={filter_options}
- Note: The actual API endpoint and parameter names may differ. This is a generalized representation.
- The example url used in the spider.py file is a search query on 'nuts'.
  
## Key Features

- Dynamic handling of product data from JSON responses
- Pagination support
- ScrapOps integration for user agent and proxy rotation
- Extraction of detailed product information including:
  - Brand and product names
  - Pricing (original and offer prices)
  - Stock availability
  - Dietary attributes and Halal status
  - Product images
  - Weight and country of origin
  - Customer ratings
  - Product category

## Data Output

The scraper outputs data with the following fields:
- Brand Name
- Product Name
- Original Price
- Offer Price
- Offer Description
- Stock Availability
- Dietary Attributes
- Halal Status
- Image URL
- Weight
- Country of Origin
- Rating
- Category

## Setup and Usage

1. Ensure you have Scrapy installed: `pip install scrapy`
2. Install ScrapOps: `pip install scrapops-scrapy-proxy-sdk`
3. Clone this repository
4. Navigate to the project directory
5. Set up your ScrapOps API key in `settings.py`
6. Run the spider: `scrapy crawl fairpricespider`

## Customization

- To adjust the number of pages scraped, modify the condition in the `parse` method:
  ```python
  if next_page <= 5:  # Change this value to scrape more or fewer pages
