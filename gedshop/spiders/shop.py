import scrapy
import requests
from pathlib import Path
from dotenv import load_dotenv
import os
path_env=Path.home()/"Secret"/".env"
load_dotenv(dotenv_path=path_env)
telegram_bot=os.environ.get("TELEGRAM_BOT")
chat_id=os.environ.get("CHAT_ID")
print(telegram_bot)
from config_ecom_scraper import GADGET, WORK, SPORT
import logging
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s",
                    filename="script_ged_shop.log")

path_env=Path.home()/"Secret"/".env.txt"
load_dotenv(dotenv_path=path_env)
telegram_bot=os.environ.get("TELEGRAM_BOT")
chat_id=os.environ.get("CHAT_ID")


class ShopSpider(scrapy.Spider):
    name = "shop"
    allowed_domains = ["gedshop.it"]
    urls_category={"gadget": GADGET, 
                   "work": WORK,
                   "sport": SPORT}
    
    def quantity_check(good_data, current_data):
        if current_data==good_data:
            result="Normal"
        elif current_data<=good_data-(good_data*0.90):
            result="Critical"
        elif current_data<=good_data-(good_data*0.15):
            result="Attention"
        else:
            result="Normal"
        return result

    def notify_allert_telegram(message):
        message=requests.get(f"https://api.telegram.org/bot{telegram_bot}/sendMessage?chat_id={chat_id}&text=")
        return message
    
    async def start(self):
        url=self.urls_category[self.category]
        yield scrapy.Request(url, callback=self.parse)

    def parse(self, response, page_number=1):
        names = response.css("div.col-12.p-09rem")
        if not names:
            return
        
        link=f"{self.urls_category[self.category]}?page={page_number+1}"
        yield response.follow(link, callback=self.parse, cb_kwargs={"page_number": page_number+1})

        for n in names:
            name=n.css("div.card-title strong::text").get()
            try:
                price=n.css("div.price::text").get().strip()
            except AttributeError:
                price=None
            item_code=n.css("p.art-cod strong::text").get()
            try:
                desc=n.css("p.fs-6.descrizione::text").getall()
                description=desc[0]
            except (IndexError, AttributeError):
                description=None
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
                        material=None
            catalogue={"Name": name, "Item Code": item_code, "Price": price, "Material": material, "Description": description}
            yield catalogue
