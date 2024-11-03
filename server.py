import json
import io
import os
from concurrent import futures

import grpc
from dotenv import load_dotenv
from gtts import gTTS

import protos.audio_pb2 as audio_pb2
import protos.audio_pb2_grpc as audio_pb2_grpc
from database import AudioDatabase

load_dotenv()

class AudioService(audio_pb2_grpc.AudioServiceServicer):
    def __init__(self):
        self.db = AudioDatabase(os.getenv("MONGODB_URI"))

    def CreateAudioFile(self, request, context):
        news_id = request.news_id
        content = request.content
        tts = gTTS(content, lang="en")
        file_name = f"{news_id}.mp3"
        tts.save(file_name)
        with open(file_name, "rb") as f:
            audio_data = f.read()
        self.db.save_audio_file(news_id, audio_data, file_name)
        os.remove(file_name)
        return audio_pb2.AudioResponse(message=f"Audio file created and saved for news_id '{news_id}'")

    def GetAudioFile(self, request, context):
        print('request:', request)
        print('news_id:', request.news_id)
        print('type(news_id):', type(request.news_id))
        audio_data = self.db.get_audio_file_from_url(request.news_id)
        if audio_data:
            return audio_pb2.AudioResponse(audio_data=audio_data)
        else:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f"Audio file for news_id '{request.news_id}' not found")
            return audio_pb2.AudioResponse()
        
    def GetAudioFileFromURL(self, request, context):
        audio_data, file_name = self.db.get_audio_file_from_url(request.url)
        if audio_data:
            return audio_pb2.AudioResponse(audio_data=audio_data, file_name=file_name)
        else:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f"Audio file for url '{request.url}' not found")
            return audio_pb2.AudioResponse()

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    audio_pb2_grpc.add_AudioServiceServicer_to_server(AudioService(), server)
    port = os.getenv('PORT', '50052')
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    print(f"Server started on port {port}")
    server.wait_for_termination()
    
if __name__ == '__main__':
    load_dotenv()
    db = AudioDatabase(os.getenv("MONGODB_URI"))
    # find all audio files in the database
    print("All audio files in the database:")
    for file in db.fs.find():
        print(file.filename)
        
    print(db.fs.find_one({"news_id": "1"}).filename)
    print(db.get_audio_file("1")[1])
    serve()