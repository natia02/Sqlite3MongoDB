from pymongo import MongoClient


class MongoDBManager:
    def __init__(self):
        self.client = MongoClient('localhost', 27017)
        self.db = self.client['university']

    def create_collection(self):
        pass

    def is_empty(self, collection_name):
        count = self.db[collection_name].count_documents({})
        return count == 0

    # in nosql database we don't have regular ids, so we don't need this method but let's implement it
    def get(self, collection_name, human_id):
        return self.db[collection_name].find_one({"_id": human_id})

    def get_list(self, collection_name, **kwargs):
        return self.db[collection_name].find(kwargs)

    def save(self, collection_name, **kwargs):
        human_id = kwargs["human_id"]
        kwargs.pop("human_id", None)
        existing_doc = self.db[collection_name].find_one({"name": kwargs["name"], "surname": kwargs["surname"],
                                                          "age": kwargs["age"]})
        if not existing_doc:
            self.db[collection_name].insert_one(kwargs)
        else:
            return human_id

        return human_id

    # def save_student_advisor(self): this method is not needed because we don't need to separate table for it.
    # other methods are written with joins and in mongodb we don't have joins so i am skipping them, too.


mongo_db = MongoDBManager()
