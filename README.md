
# MNIST GRPC Service

This project implements a GRPC service that streams MNIST samples to a client.

## Setup

1. **Clone the repository:**

    ```bash
    git clone https://github.com/Tamar-Posen/GRPC-MNIST.git
    ```

2. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

3. **Run the service:**

    ```bash
    python app/mnist_service.py
    ```

## Usage

1. **Ensure the service is running.**

2. **Run the client:**

    ```bash
    python app/mnist_client.py
    ```

    The client will connect to the service and receive streaming MNIST samples.

## Docker Containers

### Service

Build the service Docker image:

```bash
docker build -t mnist-service -f Dockerfile_service .