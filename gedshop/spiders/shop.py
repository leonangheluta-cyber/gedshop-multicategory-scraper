import scrapy
import requests
from pathlib import Path
from dotenv import load_dotenv
import os
from config_ecom_scraper import GADGET, WORK, SPORT
import logging
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s",
                    filename="script_ged_shop.log")

path_env=Path.home()/"Secret"/".env"
load_dotenv(dotenv_path=path_env)
telegram_bot=os.environ.get("TELEGRAM_BOT")
chat_id=os.environ.get("CHAT_ID")

class ShopSpider(scrapy.Spider):
    name = "shop"
    allowed_domains = ["gedshop.it"]
    urls_category={"gadget": GADGET, 
                   "work": WORK,
                   "sport": SPORT}

    def notify_allert_telegram(self, message):
        url=f"https://api.telegram.org/bot{telegram_bot}/sendMessage"
        try:
            stat=requests.get(url, params={"chat_id": chat_id, "text": message})
            status=stat.status_code
            if status !=200:
                logging.warning(f"Failed to send {message} due to status")
        except requests.exceptions.RequestException as error:
            logging.warning(f"Failed to send {message}: {error}")

    async def start(self):
        url=self.urls_category[self.category]
        yield scrapy.Request(url, callback=self.parse)

    def parse(self, response, page_number=1):
        names = response.css("div.col-12.p-09rem")
        if not names:
            logging.critical("Names not found")
            self.notify_allert_telegram("Names in page not found")
            return   
        
        link=f"{self.urls_category[self.category]}?page={page_number+1}"
        yield response.follow(link, callback=self.parse, cb_kwargs={"page_number": page_number+1})
        number_products_missing=0
        for n in names:
            name=n.css("div.card-title strong::text").get()
            if not name:
                logging.warning("Name not found")
                number_products_missing+=1
                if number_products_missing ==50:
                    self.notify_allert_telegram(f"Products missing: {number_products_missing}")
            try:
                price=n.css("div.price::text").get().strip()
            except AttributeError:
                price=None
                logging.warning(f"Price not found for {name}")
            item_code=n.css("p.art-cod strong::text").get()
            if not item_code:
                logging.warning(f"Code not foun for {name}")
            try:
                desc=n.css("p.fs-6.descrizione::text").getall()
                description=desc[0]
            except (IndexError, AttributeError):
                description=None
                logging.warning(f"Description not found for {name}")
            box=n.css("p.art-info")
            material=None
            for b in box:
                label=b.css("strong::text").get()
                if label=="Materiale":
                    try:
                        text=b.css("p::text").getall()
                        material=text[0]
                        break
                    except (IndexError, AttributeError):
                        logging.warning(f"Material not found for {name}")
                        material=None
            catalogue={"Name": name, "Item Code": item_code, "Price": price, "Material": material, "Description": description}
            yield catalogue
