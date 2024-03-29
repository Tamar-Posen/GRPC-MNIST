import grpc
import mnist_proto_pb2 as mnist_pb2
import mnist_proto_pb2_grpc as mnist_pb2_grpc
import gzip
import os
import struct
from concurrent.futures import ThreadPoolExecutor
#import boto3
#from botocore.exceptions import NoCredentialsError


class MnistService(mnist_pb2_grpc.MnistServiceServicer):
    def GetTrainingSamples(self, request, context):
        # Retrieve data from S3 implementation

        #s3_bucket = 'bucket-name'
        #images_key = 'mnist_dataset/train-images-idx3-ubyte.gz'
        #labels_key = 'mnist_dataset/train-labels-idx1-ubyte.gz'

        #try:
            #images = self.read_mnist_from_s3(s3_bucket, images_key)
            #labels = self.read_mnist_from_s3(s3_bucket, labels_key)

        script_directory = os.path.dirname(os.path.abspath(__file__))
        mnist_data_dir = os.path.join(script_directory, "mnist_dataset")

        # Load MNIST training images and labels
        images_path = os.path.join(mnist_data_dir, "train-images-idx3-ubyte.gz")
        labels_path = os.path.join(mnist_data_dir, "train-labels-idx1-ubyte.gz")

        try:
            images = self.read_mnist_images(images_path)
            labels = self.read_mnist_labels(labels_path)

            for i in range(len(images)):
                image_data = images[i]
                label = labels[i]

                yield mnist_pb2.Sample(image=image_data, label=label)

        except FileNotFoundError:
            context.set_code(grpc.StatusCode.NOT_FOUND)
            context.set_details("MNIST data files not found")
            return

        except Exception as e:
            context.set_code(grpc.StatusCode.INTERNAL)
            context.set_details(f"An error occurred: {str(e)}")
            return

    def read_mnist_images(self, file_path):
        with gzip.open(file_path, 'rb') as f:
            magic, num_images, rows, cols = struct.unpack('>IIII', f.read(16))
            image_size = rows * cols
            images = [f.read(image_size) for _ in range(num_images)]
            return images

    def read_mnist_labels(self, file_path):
        with gzip.open(file_path, 'rb') as f:
            magic, num_labels = struct.unpack('>II', f.read(8))
            labels = [struct.unpack('B', f.read(1))[0] for _ in range(num_labels)]
            return labels

    #def read_mnist_from_s3(self, bucket, key):
        #s3 = boto3.client('s3')

        #try:
            #response = s3.get_object(Bucket=bucket, Key=key)
            #content = response['Body'].read()

            #return [content[i:i + 28 * 28] for i in range(0, len(content), 28 * 28)]

        #except NoCredentialsError:
            #raise Exception("AWS credentials not available or invalid")



def serve():
    server = grpc.server(ThreadPoolExecutor(max_workers=10))
    mnist_pb2_grpc.add_MnistServiceServicer_to_server(MnistService(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()


if __name__ == '__main__':
    serve()
