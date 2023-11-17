from itemadapter import ItemAdapter
import pymongo


class WineDataProcessingPipeline:
    collection_name = "wine-infos"  # MongoDB에 저장할 컬렉션 이름

    def __init__(self, mongodb_uri, database_name):
        self.mongodb_uri = mongodb_uri
        self.database_name = database_name

    @classmethod
    def from_crawler(cls, crawler):
        mongodb_uri = crawler.settings.get(
            "MONGODB_URI"
        )  # Scrapy 설정에서 MongoDB URI 가져오기
        database_name = crawler.settings.get(
            "MONGODB_DATABASE"
        )  # Scrapy 설정에서 MongoDB 데이터베이스 이름 가져오기
        return cls(mongodb_uri, database_name)

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongodb_uri)
        self.db = self.client[self.database_name]  # 데이터베이스 선택

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        # 원산지 정보 분리
        country_region, winery = adapter["country_winery"].split(" / ")
        country, region = country_region.split(" > ")

        if adapter["food_matching"]:
            food_matching_list = [
                item.strip() for item in adapter["food_matching"].split(",")
            ]
        else:
            # food_matching 필드가 null이거나 비어있는 경우 빈 리스트를 할당
            food_matching_list = []

        if adapter["grape_variety"]:
            grape_variety_list = [
                item.strip() for item in adapter["grape_variety"].split(",")
            ]
        else:
            # food_matching 필드가 null이거나 비어있는 경우 빈 리스트를 할당
            grape_variety_list = []

        # MongoDB에 저장할 문서 형식 생성
        processed_item = {
            "_id": adapter["id"],
            "name": {
                "name_kr": adapter["name_kr"],
                "name_en": adapter["name_en"],
            },
            "type": adapter["type"],
            "description": adapter["description"],
            "origin": {
                "country": country.strip(),
                "region": region.strip(),
                "winery": winery.strip(),
            },
            "grape_variety": grape_variety_list,
            "capacity": adapter["capacity"],
            "food_matching": food_matching_list,
            "image_url": adapter["image_url"],
            "wine_attributes": {
                "sugar_level": adapter["sugar_level"],
                "acidity_level": adapter["acidity_level"],
                "body_level": adapter["body_level"],
            },
            "information": adapter["information"],
            "tip": adapter["tip"],
        }

        print("data process finished")
        # print(processed_item)

        # MongoDB에 데이터 저장
        self.db[self.collection_name].insert_one(dict(processed_item))

        return processed_item


# class MongoDBPipeline:
#     collection_name = "test"  # MongoDB에 저장할 컬렉션 이름

#     def __init__(self, mongodb_uri, database_name):
#         self.mongodb_uri = mongodb_uri
#         self.database_name = database_name

#     @classmethod
#     def from_crawler(cls, crawler):
#         mongodb_uri = crawler.settings.get(
#             "MONGODB_URI"
#         )  # Scrapy 설정에서 MongoDB URI 가져오기
#         database_name = crawler.settings.get(
#             "MONGODB_DATABASE"
#         )  # Scrapy 설정에서 MongoDB 데이터베이스 이름 가져오기
#         return cls(mongodb_uri, database_name)

#     def open_spider(self, spider):
#         self.client = pymongo.MongoClient(self.mongodb_uri)
#         self.db = self.client[self.database_name]  # 데이터베이스 선택

#     def close_spider(self, spider):
#         self.client.close()

#     def process_item(self, item, spider):
#         self.db[self.collection_name].insert_one(dict(item))
#         return item
