import unittest
from unittest.mock import patch
import grpc
from app import mnist_proto_pb2
from app.mnist_proto_pb2_grpc import MnistServiceStub
from app.mnist_service import MnistService

class MnistServiceTests(unittest.TestCase):
    def setUp(self):
        self.server = grpc.server(grpc.ThreadPoolExecutor(max_workers=10))
        self.service = MnistService()
        self.stub = MnistServiceStub(self.server)

    def tearDown(self):
        self.server.stop(None)

    @patch('mnist_service.MnistService.read_mnist_images')
    @patch('mnist_service.MnistService.read_mnist_labels')
    def test_get_training_samples_success(self, mock_read_labels, mock_read_images):
        mock_read_images.return_value = [b'fake_image_data']
        mock_read_labels.return_value = [1]

        request = mnist_proto_pb2.DataRequest()
        response_iterator = self.stub.GetTrainingSamples(request)

        response = next(response_iterator)

        self.assertEqual(response.image, b'fake_image_data')
        self.assertEqual(response.label, 1)

        mock_read_images.assert_called_once_with(self.service, 'mnist_dataset/train-images-idx3-ubyte.gz')
        mock_read_labels.assert_called_once_with(self.service, 'mnist_dataset/train-labels-idx1-ubyte.gz')

    @patch('mnist_service.MnistService.read_mnist_images', side_effect=FileNotFoundError)
    def test_get_training_samples_file_not_found(self, mock_read_images):
        mock_read_images.side_effect = FileNotFoundError

        request = mnist_proto_pb2.DataRequest()
        response_iterator = self.stub.GetTrainingSamples(request)

        with self.assertRaises(grpc.RpcError) as context:
            response = next(response_iterator)

        self.assertEqual(context.exception.code(), grpc.StatusCode.NOT_FOUND)
        self.assertEqual(str(context.exception.details()), "MNIST data files not found")

        mock_read_images.assert_called_once_with(self.service, 'mnist_dataset/train-images-idx3-ubyte.gz')


if __name__ == '__main__':
    unittest.main()
