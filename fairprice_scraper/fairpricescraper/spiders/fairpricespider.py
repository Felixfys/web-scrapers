import scrapy
import json
from ..items import FairpricescraperItem

class FairpricespiderSpider(scrapy.Spider):
    name = "fairpricespider"

    def start_requests(self):
        url = "https://website-api.omni.fairprice.com.sg/api/product/v2?algopers=prm-ppb-1%2Cprm-ep-1%2Ct-epds-1%2Ct-ppb-0%2Ct-ep-0&dId=-1049338475230325847&dSession=8sm8x8msslfr2jzuavgasu5p1r6f3hof&experiments=searchVariant-B%2CtimerVariant-Z%2CsubstitutionBSVariant-B%2Cgv-A%2Cshelflife-B%2Cds-A%2CSDND_delivery_reason-C%2Cls_comsl-B%2Cls_deltime-ogA%2Cls_deltime-feA%2Ccartfiller-a%2Ccatnav-show%2Ccatbubog-B%2Csbanner-A%2Ccount-b%2Ccam-a%2Cpriceperpiece-b%2Cls_deltime-sortA%2Cpromobanner-c%2Calgopers-b%2Cdlv_pref_mf-B%2Cdelivery_pref_ffs-B%2Cdelivery_pref_pfc-B%2Ccrtalc-B%2Crec-wtyl-dy%2Crec-fbt-dy%2Crec-r4u-ds&includeTagDetails=true&metaData=%5Bobject%20Object%5D&orderType=DELIVERY&page=1&pageType=search&query=nut&sdt=78e0d05a-fb16-4210-92f1-612e56faa835&storeId=165&url=nut" #...orderType=DELIVERY&page = {current_page}... Adjust this to change start page
        yield scrapy.Request(url=url, callback=self.parse, meta={'page': 1})
            
    def parse(self, response):
        data = json.loads(response.body)
        items = FairpricescraperItem()
         # Loop through each product in the response
        for product in data['data']['product']:
            
             # Extract relevant information
            brand_name = product['brand'].get('name', 'Unknown')
            product_name = product.get('name', 'Unknown')
            product_price = product.get('final_price', 0)
            
            if 'offers' in product and product['offers']:
                offer_price = product['offers'][0].get('price', 0) if product['offers'][0]['price'] is not None else 0
                offer_description = product['offers'][0].get('description', 'No description available')
            else:
                offer_price = 0  # Default to 0 if no offers exist
                offer_description = None
                
            product_availability = product.get('has_stock')
            dietary_attributes = product['metaData'].get("Dietary Attributes", [])  
            halal = 'Halal' in dietary_attributes
            product_image = product['images'][0] if product['images'] else 'No Image' 
            product_weight = product['metaData'].get("DisplayUnit", 'Unknown') 
            country_of_origin = product['metaData'].get("Country of Origin", 'Unknown')
            
            # Check if 'reviews' and 'statistics' are not None before accessing 'average'
            if product.get('reviews') and product['reviews'].get('statistics'): 
                average_rating = product['reviews']['statistics'].get('average')
                if average_rating is None:
                    product_rating = 0
                else:
                    product_rating = round(float(average_rating), 2)
            else:
                product_rating = 0  # Default to 0 if 'reviews' or 'statistics' is None
                
            category = product["primaryCategory"]["parentCategory"].get("name", 'Unknown')
            
            items['brand_name'] = brand_name
            items['product_name'] = product_name
            items['original_price'] = product_price
            items['offer_price'] = offer_price
            items['offer_description'] = offer_description
            items['stock'] = product_availability
            items['dietary_attributes'] = dietary_attributes
            items['halal'] = halal
            items['image_url'] = product_image
            items['weight'] = product_weight
            items['country_of_origin'] = country_of_origin
            items['rating'] = product_rating
            items['category'] = category
            yield items

        # Get the current page number from the meta data
        current_page = response.meta['page']
        next_page = current_page + 1

        # Create the next page URL by replacing the page number
        next_page_url = response.url.replace(f'page={current_page}', f'page={next_page}')

        # Send the request for the next page
        if next_page <= 5:  # Adjust this limit as needed depending on how many total pages you want to scrap
            yield scrapy.Request(url=next_page_url, callback=self.parse, meta={'page': next_page})