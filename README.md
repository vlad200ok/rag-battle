# RAG battle(WORK IN PROGRESS)

## Project description

A Dockerized RAG evaluation lab: easily compare multiple Retrieval-Augmented Generation
setups under real-world load conditions.

This project provides a modular framework for running and benchmarking different RAG
architectures using Docker.

It supports plug-and-play configurations for retrievers, vector stores, embedding
models, and LLMs. Stress tests simulate a production load to help evaluate performance,
latency, and robustness.
Features:

🔹 Docker-based isolation for reproducible experiments

🔹 Supports multiple RAG vector databases

🔹 Includes stress/load testing utilities

🔹 Easily configurable embedding models, retrievers, and LLMs

🔹 REST API for triggering queries and collecting metrics

## Installation

Start the project(NVIDIA GPU is required):

```shell
./run.sh
```

Start the project in detached mode(NVIDIA GPU is required):

```shell
./run.sh -d
```

Open Swagger [http://localhost:8080/docs](http://localhost:8080/docs)

TODO: add installation details

### UV installation

You can install UV in one of the following ways:

```shell
curl -LsSf https://astral.sh/uv/install.sh | sh
```

or

```shell
pip install uv
```

### Create a venv

```shell
uv venv
source .venv/bin/activate
```

### Adding dependencies

After adding a dependency to the `pyproject.toml` file, run the following command:

```shell
uv lock --upgrade
```

## Pre-commit hooks

I use pre-commit hooks for black.
To use the hooks, you need to install the library with its development dependencies.

### Re-initialize hooks

```shell
uv run pre-commit clean
uv run pre-commit install
```