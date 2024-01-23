import unittest
from unittest.mock import patch
import grpc
from app import mnist_proto_pb2
from app.mnist_proto_pb2_grpc import MnistServiceStub
from app.mnist_client import run

class MnistClientTests(unittest.TestCase):
    @patch('mnist_client.grpc.insecure_channel')
    def test_run_successful_response(self, mock_insecure_channel):
        mock_channel = grpc.Channel()
        mock_insecure_channel.return_value = mock_channel

        mock_stub = MnistServiceStub(mock_channel)
        with patch.object(mock_stub, 'GetTrainingSamples') as mock_get_samples:
            mock_response = [mnist_proto_pb2.Sample(image=b'fake_image_data', label=1)]
            mock_get_samples.return_value = iter(mock_response)

            run()

            mock_get_samples.assert_called_once_with(mnist_proto_pb2.DataRequest())

    @patch('mnist_client.grpc.insecure_channel')
    def test_run_error_response(self, mock_insecure_channel):
        mock_channel = grpc.Channel()
        mock_insecure_channel.return_value = mock_channel

        mock_stub = MnistServiceStub(mock_channel)
        with patch.object(mock_stub, 'GetTrainingSamples') as mock_get_samples:
            mock_get_samples.side_effect = grpc.RpcError

            run()

            mock_get_samples.assert_called_once_with(mnist_proto_pb2.DataRequest())

if __name__ == '__main__':
    unittest.main()
