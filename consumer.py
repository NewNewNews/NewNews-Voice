from confluent_kafka import Consumer, KafkaError
from confluent_kafka.schema_registry.protobuf import ProtobufDeserializer
from confluent_kafka.serialization import (
    StringDeserializer,
    SerializationContext,
    MessageField,
)
from protos import news_message_pb2, audio_pb2  # generated from .proto
from gtts import gTTS
import os
from database import AudioDatabase
from dotenv import load_dotenv

# from confluent_kafka.schema_registry import SchemaRegistryClient

def create_audio_file(url, content):
    print('processing url:', url)
    tts = gTTS(content, lang="th")
    file_name = f"audio.mp3"
    tts.save(file_name)
    with open(file_name, "rb") as f:
        audio_data = f.read()
    import uuid
    db.save_audio_file(str(uuid.uuid4()), audio_data, url)
    print('audio file created and saved for url:', url)
    os.remove(file_name)
    return
    return audio_pb2.AudioResponse(message=f"Audio file created and saved for url '{url}'")
    
def main():
    # schema_registry_conf = {
    #     "url": "http://localhost:8081"
    # }  # Change to your schema registry URL
    # schema_registry_client = SchemaRegistryClient(schema_registry_conf)

    protobuf_deserializer = ProtobufDeserializer(
        news_message_pb2.NewsMessage,
        # schema_registry_client,
        conf={"use.deprecated.format": True},
    )
    string_deserializer = StringDeserializer("utf_8")

    consumer_conf = {
        "bootstrap.servers": os.environ.get("KAFKA_BROKER", "localhost:9092"),
        "group.id": "news_group",
        "auto.offset.reset": "earliest",
    }

    consumer = Consumer(consumer_conf)
    consumer.subscribe(["news_topic"])

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
            print(f"Consumed record with key: {key}")
            print('news_message:', news_message)
            
        create_audio_file(news_message.url, news_message.data)

    consumer.close()


if __name__ == "__main__":
    load_dotenv()
    db = AudioDatabase(os.getenv("MONGODB_URI"))
    main()
