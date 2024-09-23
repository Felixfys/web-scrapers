import scrapy
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from scrapy import Selector
import time

class ShengsiongspiderSpider(scrapy.Spider):
    name = "shengsiongspider"
    allowed_domains = ["shengsiong.com.sg"]
    start_urls = ["https://shengsiong.com.sg/search/nut"]

    def __init__(self, *args, **kwargs):
        super(ShengsiongspiderSpider, self).__init__(*args, **kwargs)

        # Set up Selenium with WebDriver Manager
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")  # Set browser window size

        # Initialize ChromeDriver using WebDriver Manager
        self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

    def scroll_to_bottom(self):
        """Scroll to the bottom of the page to load more items."""
        #Adjust accordingly based on performance
        SCROLL_PAUSE_TIME = 2 

        last_height = self.driver.execute_script("return document.body.scrollHeight")
        
        while True:
            # Scroll down to the bottom
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            
            # Wait for new content to load
            time.sleep(SCROLL_PAUSE_TIME)
            
            # Calculate new scroll height and compare with last scroll height
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            
            if new_height == last_height:
                # If the scroll height hasn't changed, all items have been loaded
                break
            last_height = new_height

    def parse(self, response):
        # Open the URL using Selenium
        self.driver.get(self.start_urls[0])

        # WebDriverWait to ensure the product container is fully loaded
        wait = WebDriverWait(self.driver, 30)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.col-lg-2")))

        # Scroll to the bottom of the page to load all products
        self.scroll_to_bottom()

        # Once all products are loaded, get the page source
        html = self.driver.page_source

        # Create a Scrapy Selector from the Selenium page source
        sel = Selector(text=html)

        # Select product elements and extract the links
        product_elements = sel.css('div.col-lg-2 a.product-preview')
        
        for product_element in product_elements:
            # Extract the product link
            product_link = product_element.css('::attr(href)').get()
            
            # Use Selenium to click on the product link, which opens the modal
            product_selector = self.driver.find_element(By.CSS_SELECTOR, 'a[href="{}"]'.format(product_link))
            product_selector.click()
            
            # Wait for modal to load
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.product-summary")))

            # After the modal is loaded, get the updated page source with the modal content
            modal_html = self.driver.page_source
            modal_sel = Selector(text=modal_html)
            
         
           # Extract product details from the modal
            name_parts = modal_sel.css('div.product-title.font-2xl::text').getall()
            name = ' '.join(name_parts).strip() if name_parts else None
            
            uom = modal_sel.css('div.product-uom::text').get()

            # Pricing logic: handling both normal and discounted prices
            promo_price = modal_sel.css('span.promo-price.font-2xl::text').get()
            previous_price = modal_sel.css('strike.previous-price::text').get()
            normal_price = modal_sel.css('div.product-price-tag div.font-2xl::text').get()

            # Determine final pricing: normal price (non-sale) or discounted + previous price (sale)
            if promo_price and previous_price:
                discounted_price = promo_price.strip()
                final_normal_price = previous_price.strip()
            else:
                discounted_price = None
                final_normal_price = normal_price.strip() if normal_price else None

            origin = modal_sel.css('div.row div.pb-2.title:contains("Origin") + div.col-12.col-sm-9.col-md-8::text').get()
            dietary = modal_sel.css('div.row div.pb-2.title:contains("Dietary") + div.col-12.col-sm-9.col-md-8 div.dietary-habit-tag::text').get()
            image_url = modal_sel.css('img::attr(src)').get()

            # Pricing logic: Promo price and normal price
            yield {
                'name': name.strip() if name else None,
                'weight': uom.strip() if uom else None,
                'normal_price': final_normal_price,
                'discounted_price': discounted_price,
                'origin': origin.strip() if origin else None,
                'dietary': dietary.strip() if dietary else None,
                'image_url': image_url.strip() if image_url else None
            }
            
            # Close the modal by clicking the close button
            close_button = self.driver.find_element(By.CSS_SELECTOR, 'button.close-button.border-0.font-2xl.btn.btn-default')
            self.driver.execute_script("arguments[0].click();", close_button)

            # Wait for the modal to close before proceeding to the next product
            time.sleep(1)  # Small delay to ensure modal is closed before next interaction
            
    def get_product_detail(self, sel, detail_type):
        """Helper function to get specific product details from the modal."""
        detail = sel.css(f'div.row div.pb-2.title:contains("{detail_type}") + div.col-12.col-sm-9.col-md-8::text').get()
        return detail.strip() if detail else None
        
    def closed(self, reason):
        self.driver.quit()
