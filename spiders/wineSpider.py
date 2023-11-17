import scrapy
from scrapy import Spider

from wine_scraper.items import WineItem
import re


class wineSpider(scrapy.Spider):
    name = "wine-spider"

    base_url = "https://www.shinsegae-lnb.com/html/product/wineView.html?idx="

    def start_requests(self):
        # 범위내 idx 값을 가진 와인 페이지에 대한 요청 생성
        for idx in range(2182, 2130, -1):
            url = f"{self.base_url}{idx}"
            yield scrapy.Request(url, self.parse)

    def parse(self, response):
        page_source = response.text

        item = WineItem()

        # idx 정규표현식
        match = re.search(r"idx=(\d+)", response.url)
        idx = match.group(1) if match else None

        item["id"] = idx
        item["type"] = response.css("span.country + span::text").get()

        # right 데이터 추출
        for product in response.css(".left"):
            item["name_kr"] = product.css("h3::text").get()
            item["name_en"] = product.css(".nameEng::text").get()
            item["description"] = product.css(".des::text").get()

        # left 데이터 추출
        food_matching_flag = 0
        for product in response.css(".right"):
            # 각 테이블 데이터 추출
            rows = product.css("table tr")
            for row in rows:
                header = row.css("th::text").get()
                value = row.css("td::text").get()

                if header == "Country / Winery":
                    item["country_winery"] = value
                elif header == "Grape Variety":
                    item["grape_variety"] = value
                elif header == "Capacity":
                    item["capacity"] = value
                elif header == "Food Matching":
                    item["food_matching"] = value
                    food_matching_flag = 1

        if food_matching_flag == 0:
            item["food_matching"] = None

        # 이미지 추출
        image_url = response.css(".productInner.img img::attr(src)").get()
        item["image_url"] = image_url

        # 당도, 산도, 바디 추출
        features_div = response.css(".features")

        sugar_level_raw = (
            features_div.css('dl:contains("당도") dd').css("span.on::attr(title)").get()
        )
        sugar_level = sugar_level_raw[0] if sugar_level_raw else None

        acidity_level_raw = (
            features_div.css('dl:contains("산도") dd').css("span.on::attr(title)").get()
        )
        acidity_level = acidity_level_raw[0] if acidity_level_raw else None

        body_level_raw = (
            features_div.css('dl:contains("바디") dd').css("span.on::attr(title)").get()
        )
        body_level = body_level_raw[0] if body_level_raw else None
        print(sugar_level)
        print(acidity_level)
        print(body_level)

        item["sugar_level"] = sugar_level
        item["acidity_level"] = acidity_level
        item["body_level"] = body_level

        # info,tip추출
        second_product = response.css(".productInner.col2")[1]

        print(second_product.get())
        item["information"] = second_product.css(".textDes p::text").get()

        # Tip 섹션의 텍스트 추출
        item["tip"] = second_product.css(".textDes::text").get()

        yield item
