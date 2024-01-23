import grpc
import mnist_proto_pb2 as mnist_pb2
import mnist_proto_pb2_grpc as mnist_pb2_grpc
import os


def run():
    server_address = os.environ.get('MNIST_SERVER_ADDRESS', 'localhost')
    channel = grpc.insecure_channel(f'{server_address}:50051')
    client = mnist_pb2_grpc.MnistServiceStub(channel)
    request = mnist_pb2.DataRequest()

    try:
        responses = client.GetTrainingSamples(request)
        for response in responses:
            print(f"Received image with label: {response.label}")

    except grpc._channel._InactiveRpcError as e:
        print(f"Error: {e.details()}")


if __name__ == '__main__':
    run()
