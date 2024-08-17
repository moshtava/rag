
class CollectionExistsError(Exception):
   def __init__(self, collection_name):
    super().__init__(f"The collection '{collection_name}' already exists.")
    self.collection_name = collection_name
