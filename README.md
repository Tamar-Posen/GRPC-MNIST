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

## Running with Docker

### Service Container

1. **Build the service Docker image:**

    ```bash
    docker build -t mnist-service -f Dockerfile_service .
    ```

2. **Run the service container:**

    ```bash
    docker run -p 50051:50051 mnist-service
    ```

### Client Container

1. **Build the client Docker image:**

    ```bash
    docker build -t mnist-client -f Dockerfile_client .
    ```

2. **Run the client container, specifying the server address:**

    Replace `<host-ip>` with the actual IP address where the server container is running.

    ```bash
    docker run -e MNIST_SERVER_ADDRESS=<host-ip> mnist-client
    ```

## Running Without Docker

### Service

1. **Ensure the service is running:**

    ```bash
    python app/mnist_service.py
    ```

### Client

1. **Ensure the service is running.**

2. **Run the client:**

    ```bash
    python app/mnist_client.py
    ```

    The client will connect to the service and receive streaming MNIST samples.
