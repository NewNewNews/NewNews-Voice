from pymongo import MongoClient
import gridfs

class AudioDatabase:
    def __init__(self, db_url, db_name="audio_db"):
        self.client = MongoClient(db_url)
        self.db = self.client[db_name]
        self.fs = gridfs.GridFS(self.db)

    def get_audio_file(self, news_id):
        file = self.fs.find_one({"news_id": news_id})
        if file:
            return file.read(), file.filename
        return None, None

    def save_audio_file(self, news_id, audio_data):
        filename = f"{news_id}.mp3"
        self.fs.put(audio_data, filename=filename, news_id=news_id)