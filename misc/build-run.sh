#!/bin/bash
# this build two vulkan llamas and start the qwen35 on (8033) and embedded nomic (8034) models
# for fat vss llm laa zu

cd ./

# fetch and build llama.cpp
git clone --depth=1 https://github.com/ggerganov/llama.cpp
cp -r llama.cpp llama-vulkan
cp -r llama.cpp llama-embedded

cd llama-vulkan && cmake -B build -DGGML_VULKAN=1 && cmake --build build --config Release -j $(grep -c ^processor /proc/cpuinfo)
RUN cd llama-embedded && cmake -B build -DGGML_VULKAN=1 && cmake --build build --config Release -j $(grep -c ^processor /proc/cpuinfo)

# fetch and install qdrant vector indexing service 
cd ./
docker run -d --name qdrant \
  --restart unless-stopped \
  -p 6333:6333 \
  -p 6334:6334 \
  -v ~/qdrant_storage:/qdrant/storage \
  qdrant/qdrant

# fetch and run whispr
apt update
apt install docker.io docker-compose-v2 git -y

cd ./
git clone https://github.com/mwhesse/whisperx-assistant-vscode.git ~/.whisperx-assistant
cd ~/.whisperx-assistant && docker compose --profile external up -d


# run llms on 8033 and 8034 for embedded indexing

cd ./
./llama-vulkan/build/bin/llama-server   -m /media/aryan/nvme/models/llama.cpp/Qwen3.5-35B-A3B-Q4_K_S.gguf   --jinja   --device Vulkan0,Vulkan2   --host 0.0.0.0   -np 1   --port 8033   -c 128000   -fa on  &&
./llama-embedded/build/bin/llama-server   -m /media/aryan/nvme/models/llama.cpp/nomic-embed-text-v1.5.Q6_K.gguf   --jinja   --device Vulkan0,Vulkan2   --host 0.0.0.0   -np 1   --port 8034  -fa on --embedding &&
