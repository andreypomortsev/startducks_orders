# Starducks Scalable Order Processing System

This project provides a scalable order processing system for a coffee shop, inspired by Starbucks. This repository contains the source code for a scalable order processing system inspired by Starbucks. The system utilizes FastAPI to handle HTTP requests, Redis for message queuing, and PostgreSQL for managing inventory.

## File Structure

```
startducks_orders/
├── api/
│   ├── Dockerfile
│   ├── Dockerfile.test
│   ├── main.py
│   ├── requirements.txt
│   └── tests/
│       ├── __init__.py
│       ├── test_main.py
│       └── test_data.sql
├── worker/
│   ├── __init__.py
│   ├── Dockerfile
│   ├── worker.py
│   └── requirements.txt
├── database/
│   ├── Dockerfile
│   └── init.sql
├── docker-compose.yml
├── LICENSE
└── README.md

```

## Getting Started

### Prerequisites

- Docker
- Docker Compose

### Running the Services

1. Clone the repository:
   ```sh
   git clone https://github.com/andreypomortsev/startducks_orders.git
   cd startducks_orders
   ```

2. Build and start the services:
   ```sh
   docker-compose up --build
   ```

3. The FastAPI service will be available at `http://localhost:8000`.

## Endpoints

- `POST /order`: Create a new order
  - Request Body: `{"preferences": ["Эспрессо", "Капучино"]}`
  - Response: `{"result": "Order <order_id> received"}`

## Authors

- [Andrei Pomortsev](https://www.linkedin.com/in/andreypomortsev/)

## License

This project is licensed under the MIT License - see the [LICENSE](.LICENSE) file for details.
```

This structure and the provided Docker configurations will help you containerize and manage the services efficiently. The use of Docker Compose allows for easy orchestration of the different services involved in the system.
