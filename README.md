<img width="1536" height="1024" alt="ChatGPT Image Jan 1, 2026, 12_55_47 PM" src="https://github.com/user-attachments/assets/64036380-01d8-4b3a-9152-eff641577d4c" />

# ThereminQ-llama: Baking a Quantum Layer Cake

This repository is dedicated to extending GGUF llama Large Language Models (LLMs) with Quantum Computing (QC) data and agentic capabilities.

## Table of Contents

- [Overview](#overview)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [Dockerfiles](#dockerfiles)
- [Runfiles](#runfiles)
- [Misc Scripts](#misc-scripts)
- [Contributing](#contributing)
- [License](#license)
- [Credits](#credits)

## Overview

ThereminQ-llama integrates several cutting-edge technologies to create a powerful and versatile platform for QC-enhanced AI. The core components of the stack include:

- **Qrackmin:** A library for quantum simulation.
- **llama.cpp:** A library for running LLMs.
- **Open Interpreter:** A tool for enabling agentic capabilities.

The project is still in its alpha stage, with new features and functionalities being actively developed.

## Getting Started

To get started with ThereminQ-llama, you will need to have Docker installed on your system. You can then pull the desired Docker image from the Docker Hub and run it using the following command:

1. **Install Docker:** If you don't have Docker installed, please follow the official instructions for your operating system: [https://docs.docker.com/get-docker/](https://docs.docker.com/get-docker/)

2. **Pull the Docker Image:** Pull the desired Docker image from Docker Hub. For example, to pull the `latest` image, you would run:

   ```bash
   docker pull twobombs/thereminq-llama:latest
   ```

3. **Run the Docker Container:** Run the Docker container using the following command. This command maps the necessary ports and mounts a volume for your models.

   ```bash
   docker run --gpus all --device=/dev/kfd --device=/dev/dri:/dev/dri -v /path-to-/models:/text-generation-webui/models -p 5000:5000 -p 5173:5173 -p 5601:5601 -p 6080:6080 -p 7860:7860 -p 7861:7861 -p 8501:8501 -p 8081:8081 -p 9000:9000 -d twobombs/thereminq-llama[:tag]
   ```

## Usage

The project offers several Docker tags, each providing a different set of functionalities. Here are some examples of how to use them:

- **`latest`**: This is the most comprehensive image, including all QC/AI dependencies and a Llama3 model. It is a great starting point for exploring the full capabilities of the project.

- **`cli`**: This image is ideal for users who prefer to work from the command line. It provides compiled versions of Llama.cpp, allowing you to perform tasks such as model conversion and quantization directly.

- **`chatui`**: If you're looking for a user-friendly web interface, this image is for you. It includes the text-generation-webui and Stable Diffusion, allowing you to chat with the LLM and generate images.

- **`agent`**: This image provides a powerful agentic environment with the OpenInterpreterUI and Ollama3 integration. It is perfect for developing and experimenting with autonomous agents.

- **`big-agency`**: For more advanced multi-agent applications, this image includes Autogen Studio, which allows you to build and manage complex agentic workflows.

## Dockerfiles

The `Dockerfiles/` directory contains the Dockerfiles used to build the various Docker images for this project. Each Dockerfile is tailored to a specific use case, from running a simple CLI to a full-fledged agentic UI.

- **`Dockerfile`**: The base image for the project. It includes all the necessary dependencies for running the core components of the stack, such as `qrack-dev`, `huggingface_hub`, `open-interpreter`, `alloy`, `llama-cpp-python`, `thereminq-bonsai`, `ollama`, and `codecarbon`.

- **`Dockerfile-agent`**: Extends the base image with additional tools for agentic capabilities. This includes quantum computing libraries like `pyqrack`, `vllm`, and `qiskit`, as well as the `OpenInterpreterUI` for a web-based interface.

- **`Dockerfile-big-agency`**: Extends the `agent` image with `autogenstudio`, a tool for building and managing multi-agent systems.

- **`Dockerfile-chatui`**: Sets up a web-based chat interface with text-to-speech, web RAG, and image generation capabilities. It includes `text-generation-webui`, `stable-diffusion-webui`, and `easy-diffusion`.

- **`Dockerfile-chemistry`**: Extends the base image with tools for quantum chemistry, including `esm`, `qiskit-nature`, and `chemps2`.

- **`Dockerfile-chronos`**: Extends the base image with time-series forecasting capabilities, including Amazon's `chronos` and IBM's `granite-tsfm`.

- **`Dockerfile-cli`**: Focused on providing a command-line interface for `llama.cpp`. It builds multiple versions of `llama.cpp` (including one with CUDA support) and installs dependencies for model conversion and merging.

- **`Dockerfile-diffusion`**: Sets up a Stable Diffusion web UI for image generation.

## Runfiles

The `runfiles/` directory contains a collection of scripts for running different components of the ThereminQ-llama stack. These scripts are designed to be executed within the Docker containers and provide a convenient way to start and manage the various services.

- **`run-agent`**: This script starts the agentic environment. It initializes a virtual desktop environment, launches the OpenInterpreterUI, and starts the Ollama service with the Llama 3 model.

- **`run-big-agency`**: This script is similar to `run-agent`, but it also starts Autogen Studio, a tool for building and managing multi-agent systems.

- **`run-chatui`**: This script launches the web-based chat interface. It starts the text-generation-webui and koboldcpp, providing a user-friendly way to interact with the LLM.

- **`run-chemistry`**: This script sets up the environment for quantum chemistry experiments. It starts a virtual desktop and runs the `run-hydrogen.py` script, which simulates a hydrogen atom using Qiskit.

- **`run-diffusion`**: This script is a placeholder and does not currently have any functionality.

- **`run-hydrogen.py`**: This Python script simulates a hydrogen atom using Qiskit and the VQE algorithm. It is executed by the `run-chemistry` script.

- **`run-llama`**: This script is the main entrypoint for the base Docker image. It starts a virtual desktop, precompiles the Qrack kernels, and starts the Ollama service.

- **`run-qtensor`**: This script runs a benchmark for generating and loading quantum circuit tensors.

- **`run-sd`**: This script launches the Stable Diffusion web UI and Easy Diffusion for image generation.

## Misc Scripts

The `misc/` directory contains a variety of utility scripts for tasks such as:

- **`browsefiles`**: This script is a placeholder and does not currently have any functionality.

- **`config.yaml`**: This is a configuration file for Easy Diffusion.

- **`convert&quantize.sh`**: This script is a utility for converting and quantizing Hugging Face models to the GGUF format.

- **`copperai.env`**: This is a configuration file for various services, including OpenAI, TTS, and database connections.

- **`csv2json.sh`**: This script is a utility for converting CSV files to JSON.

- **`fetch-bins.sh`**: This script downloads a large number of pre-trained language models from Hugging Face.

- **`opensearch.sh`**: This script launches OpenSearch and OpenSearch Dashboards using Docker.

- **`pull.sh`**: This script downloads a large language model from Hugging Face.

- **`run-hydrogen.py`**: This Python script simulates a hydrogen atom using Qiskit and the VQE algorithm. It is a duplicate of the script in the `runfiles` directory.

## Contributing

We welcome contributions to ThereminQ-llama! If you would like to contribute, please follow these steps:

1. **Fork the repository:** Create a fork of the repository to your own GitHub account.

2. **Create a new branch:** Create a new branch for your changes.

3. **Make your changes:** Make your desired changes to the codebase.

4. **Submit a pull request:** Submit a pull request to the `main` branch of the original repository.

Please ensure that your code adheres to the existing coding style and that you have tested your changes thoroughly.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Credits

- **Dan Strano:** For his work on Qrack.
- **Georgi Gerganov:** For his work on llama.cpp.
- **Open Interpreter:** For their work on the Open Interpreter project.
- **AutoGen Studio:** For their work on AutoGen Studio.

... and their respective contributors.

![Untitled](https://user-images.githubusercontent.com/12692227/232248160-f4c2a3aa-fd19-4b62-b6f2-532ec44ca0e3.png)

*Poem generated by ChatGPT 3*
