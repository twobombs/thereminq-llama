FROM twobombs/qrackmin:pocl

# fetch dependancies
RUN export DEBIAN_FRONTEND=noninteractive && apt update && apt install -y git python3-pip mc wget libopenblas-dev libclblast-dev

#fetch llama.cpp
RUN git clone https://github.com/ggerganov/llama.cpp
RUN cp -r llama.cpp llama-cublas
RUN cp -r llama.cpp llama-clblast

# build all versions
RUN cd llama.cpp && make LLAMA_OPENBLAS=1
RUN cd llama-cublas && make LLAMA_CUBLAS=1
RUN cd llama-clblast && make LLAMA_CLBLAST=1

#load default model and symlink
RUN cd llama.cpp/models && wget https://huggingface.co/Pi3141/alpaca-native-13B-ggml/resolve/main/ggml-model-q8_0.bin
RUN ln -s /llama.cpp/models/ggml-model-q8_0.bin /llama-cublas/models/ggml-model-q8_0.bin
RUN ln -s /llama.cpp/models/ggml-model-q8_0.bin /llama-clblast/models/ggml-model-q8_0.bin

# test build
RUN cd llama.cpp && ./main -m ./models/ggml-model-q8_0.bin -p "explain the negative energy spike when teleporting a qubit according to ER=EPR" -n 512

ENV NVIDIA_VISIBLE_DEVICES all
ENV NVIDIA_DRIVER_CAPABILITIES graphics,utility,compute
ENTRYPOINT /root/run
