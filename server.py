import json
import io
import os
from concurrent import futures

import grpc
import pika
from dotenv import load_dotenv
from gtts import gTTS

import protos.audio_pb2 as audio_pb2
import protos.audio_pb2_grpc as audio_pb2_grpc
from database import AudioDatabase

load_dotenv()

class AudioService(audio_pb2_grpc.AudioServiceServicer):
    def __init__(self):
        self.db = AudioDatabase(os.getenv("MONGODB_URL"))

    def GetAudioFile(self, request, context):
        audio_data, file_name = self.db.get_audio_file(request.news_id)
        if audio_data:
            return audio_pb2.AudioResponse(audio_data=audio_data, file_name=file_name)
        else:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f"Audio file for news_id '{request.news_id}' not found")
            return audio_pb2.AudioResponse()

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    audio_pb2_grpc.add_AudioServiceServicer_to_server(AudioService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    print("Server started on port 50051")
    server.wait_for_termination()
    
if __name__ == '__main__':
    serve()