import scrapy


class WineItem(scrapy.Item):
    id = scrapy.Field()

    name_kr = scrapy.Field()
    name_en = scrapy.Field()

    type = scrapy.Field()
    description = scrapy.Field()

    origin = scrapy.Field()
    country_winery = scrapy.Field()
    grape_variety = scrapy.Field()
    capacity = scrapy.Field()
    food_matching = scrapy.Field()

    image_url = scrapy.Field()

    sugar_level = scrapy.Field()
    acidity_level = scrapy.Field()
    body_level = scrapy.Field()

    information = scrapy.Field()
    tip = scrapy.Field()
