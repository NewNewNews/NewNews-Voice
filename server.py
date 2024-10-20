import json
import io
import os
from concurrent import futures

import grpc
import os
from dotenv import load_dotenv
from gtts import gTTS
import protos.audio_pb2 as audio_pb2
import protos.audio_pb2_grpc as audio_pb2_grpc
from database import AudioDatabase
import time
from confluent_kafka import Consumer, KafkaError
from confluent_kafka.schema_registry.protobuf import ProtobufDeserializer
from confluent_kafka.serialization import (
    StringDeserializer,
    SerializationContext,
    MessageField,
)
from proto import news_message_pb2, audio_pb2, audio_pb2_grpc
import threading

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
        return audio_pb2.AudioResponse(
            message=f"Audio file created and saved for news_id '{news_id}'"
        )

    def GetAudioFile(self, request, context):
        print("request:", request)
        print("news_id:", request.news_id)
        print("type(news_id):", type(request.news_id))
        audio_data, file_name = self.db.get_audio_file(request.news_id)
        print("file_name:", file_name)
        if audio_data:
            return audio_pb2.AudioResponse(audio_data=audio_data, file_name=file_name)
        else:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details(f"Audio file for news_id '{request.news_id}' not found")
            return audio_pb2.AudioResponse()


def kafka_consumer_thread(audio_service):
    protobuf_deserializer = ProtobufDeserializer(
        news_message_pb2.NewsMessage, conf={"use.deprecated.format": True}
    )
    string_deserializer = StringDeserializer("utf_8")

    consumer_conf = {
        "bootstrap.servers": "localhost:9092",
        "group.id": "news_group",
        "auto.offset.reset": "earliest",
    }

    consumer = Consumer(consumer_conf)
    consumer.subscribe(["news_topic"])

    try:
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                continue

            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    continue
                else:
                    print(msg.error())
                    break

            key = string_deserializer(
                msg.key(), SerializationContext(msg.topic(), MessageField.KEY)
            )
            news_message = protobuf_deserializer(
                msg.value(), SerializationContext(msg.topic(), MessageField.VALUE)
            )

            if news_message is not None:
                print(f"Consumed record with key {key}: {news_message}")
                # Here you would typically call a method on audio_service to process the news message
                # For example:
                # audio_service.process_news(news_message)
    finally:
        consumer.close()


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    audio_pb2_grpc.add_AudioServiceServicer_to_server(AudioService(), server)
    server.add_insecure_port("[::]:50052")
    server.start()
    print("Server started on port 50052")
    server.wait_for_termination()

    # Did not test yet. TODO connect to kafka and start thread
    # audio_service = AudioService()
    # kafka_thread = threading.Thread(target=kafka_consumer_thread, args=(audio_service,))
    # kafka_thread.start()

    # try:
    #     while True:
    #         time.sleep(86400)
    # except KeyboardInterrupt:
    #     server.stop(0)


if __name__ == "__main__":
    load_dotenv()
    db = AudioDatabase(os.getenv("MONGODB_URI"))
    # find all audio files in the database
    print("All audio files in the database:")
    for file in db.fs.find():
        print(file.filename)

    print(db.fs.find_one({"news_id": "1"}).filename)
    print(db.get_audio_file("1")[1])
    serve()
