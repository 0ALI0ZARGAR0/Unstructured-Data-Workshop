# Hands-On Unstructured Data: From Logs to Semantic Search

## Workshop Overview

A practical workshop demonstrating tools and techniques for handling and extracting value from unstructured data like application logs and raw text, using Dockerized environments.

### Learning Objectives

- Set up a log aggregation pipeline using Loki, Promtail, and Grafana.
- Perform real-time log querying and analysis using LogQL.
- Understand the basics of vector embeddings and semantic search.
- Set up a vector database (Qdrant) and index text data.
- Perform semantic searches on text data using a sentence-transformer model.
- Gain experience with Docker Compose for deploying multi-service applications.

### Target Audience

Developers, DevOps engineers, data analysts, and anyone interested in practical applications of unstructured data processing.

### Prerequisites

- Basic understanding of Docker and command-line interface.
- Docker Desktop (or equivalent) installed and running.
- Python (3.8+) and pip installed.
- Internet access (for pulling Docker images and Python packages).

---

## Directory Structure

```
.
├── docker-compose.yml
├── promtail-config.yaml
├── grafana-provisioning/
│   └── datasources/
│       └── loki-datasource.yaml
├── log-generator/
│   ├── app.py
│   └── Dockerfile
├── semantic_search_demo.py
└── WORKSHOP.md
```

---

## Part 1: Log Management with Loki & Grafana

### 1. Start the Log Pipeline

Build and start the log generator and supporting services:

```sh
docker-compose up -d --build log-generator
```

This will also start Loki, Promtail, Grafana, and Qdrant.

### 2. Access Grafana

- Open your browser and go to: [http://localhost:3000](http://localhost:3000)
- **Login:**
  - Username: `admin`
  - Password: `admin`

### 3. Add Loki as a Data Source (if not auto-provisioned)

- Go to **Configuration > Data Sources**
- Click **Add data source**
- Choose **Loki**
- Set URL to `http://loki:3100`
- Click **Save & Test**

### 4. Explore Logs

- Go to **Explore** (compass icon)
- Select **Loki** as the data source
- Try these LogQL queries:

```
{container="log_generator_service"}
{container="log_generator_service"} | json | level="ERROR"
{container="log_generator_service"} |= "payment"
count_over_time({container="log_generator_service"}[5m])
```

- **Observe:**
  - Real-time log flow
  - Filtering by log level, message content
  - Aggregations over time

---

## Part 2: Semantic Search with Qdrant

### 1. Ensure Qdrant is Running

Qdrant is started as part of `docker-compose up -d`. Confirm with:

```sh
docker-compose ps
```

You should see `qdrant_service` running and port 6333 mapped.

### 2. Set Up Python Environment

Install required libraries:

```sh
pip install sentence-transformers qdrant-client torch torchvision torchaudio
```

> **Note for Apple Silicon (M1/M2):**
> If you encounter issues installing `torch`, see: https://pytorch.org/get-started/locally/

### 3. Run the Semantic Search Demo

```sh
python semantic_search_demo.py
```

- The script will:
  - Load a small embedding model
  - Connect to Qdrant
  - Index a set of sample words
  - Enter an interactive search loop

#### Example Search Terms

- `royal female`
- `fruit`
- `vehicle`
- `sadness`
- `computer peripheral`
- `hot season`

- **Observe:**
  - Results are based on meaning, not just keyword match
  - Similarity scores for each result

---

## Cleanup

To stop and remove all containers and volumes:

```sh
docker-compose down -v
```

- The `-v` flag also removes named and anonymous volumes (e.g., Qdrant data).

---

## Key Concepts

### What is Unstructured Data?

- Data that does not have a predefined data model or is not organized in a pre-defined manner (e.g., logs, text, images).

### Log Aggregation

- Collecting logs from multiple sources for centralized analysis.
- **Loki** stores and indexes logs; **Promtail** ships logs from containers.

### LogQL

- Query language for Loki, similar to Prometheus queries but for logs.
- Supports filtering, parsing, and aggregations.

### Vector Embeddings

- Represent text as high-dimensional numeric vectors capturing semantic meaning.

### Semantic Search

- Search by meaning, not just keywords, using vector similarity.

### Vector Database (Qdrant)

- Stores and searches high-dimensional vectors efficiently.

---

## Troubleshooting Tips

### Docker

- **Port conflicts:** Make sure ports 3000 (Grafana), 3100 (Loki), 6333 (Qdrant REST) are free.
- **Docker daemon not running:** Start Docker Desktop or your Docker service.
- **Image pull failures:** Check your internet connection.

### Python

- **Package install errors:**
  - For `torch` on M1/M2 Macs, see [PyTorch install guide](https://pytorch.org/get-started/locally/).
- **Script errors:** Ensure Qdrant is running and accessible at `localhost:6333`.

### Networking

- **Grafana can't connect to Loki:** Check that both services are running and ports are mapped.
- **Python script can't connect to Qdrant:** Ensure Qdrant is up and port 6333 is mapped to localhost.

---

🚀
