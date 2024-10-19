import grpc
import protos.audio_pb2 as audio_pb2
import protos.audio_pb2_grpc as audio_pb2_grpc

def run():
    with grpc.insecure_channel('localhost:50052') as channel:
        stub = audio_pb2_grpc.AudioServiceStub(channel)
        
        # Send news content
        news_id = input("Enter the news ID: ")
        # content = input("Enter the news content: ")
        # response = stub.ReceiveNewsContent(audio_pb2.NewsContentRequest(news_id=news_id, content=content))
        # print(f"News content sent: {response.message}")
        
        # Retrieve audio file
        print('news_id:', news_id)
        input("Press Enter to retrieve the audio file...")
        response = stub.GetAudioFile(audio_pb2.AudioRequest(news_id=news_id))
        print(response)
        if response.audio_data:
            print(f"Received audio file: {response.file_name}")
            print(f"Audio data size: {len(response.audio_data)} bytes")
            # Save the audio file
            with open(f"received_{response.file_name}", "wb") as f:
                f.write(response.audio_data)
            print(f"Audio file saved as 'received_{response.file_name}'")
        else:
            print("Audio file not found")

if __name__ == '__main__':
    run()