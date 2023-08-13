FROM twobombs/qrackmin

# fetch dependancies
RUN export DEBIAN_FRONTEND=noninteractive && apt update && apt install -y git python3-pip mc wget libopenblas-dev libclblast-dev

#fetch llama.cpp
RUN git clone https://github.com/ggerganov/llama.cpp
RUN cp -r llama.cpp llama-openblas
RUN cp -r llama.cpp llama-cublas
RUN cp -r llama.cpp llama-clblast

# build all versions
RUN cd llama.cpp && make -j
RUN cd llama-openblas && cmake . && make LLAMA_OPENBLAS=1 all
RUN cd llama-cublas && cmake -DGGML_CUBLAS=ON . && make LLAMA_CUBLAS=1 all
RUN cd llama-clblast && cmake -DGGML_CLBLAST=ON . && make LLAMA_CLBLAST=1 all

#load default model and symlink
RUN cd llama.cpp/models && wget https://huggingface.co/TheBloke/orca_mini_v2_13b-GGML/resolve/main/orca_mini_v2_13b.ggmlv3.q2_K.bin
# https://huggingface.co/Pi3141/alpaca-native-13B-ggml/resolve/main/ggml-model-q8_0.bin
RUN ln -s /llama.cpp/models/ggml-model-q8_0.bin /llama-cublas/models/ggml-model-q8_0.bin
RUN ln -s /llama.cpp/models/ggml-model-q8_0.bin /llama-clblast/models/ggml-model-q8_0.bin
RUN ln -s /llama.cpp/models/ggml-model-q8_0.bin /llama-openblas/models/ggml-model-q8_0.bin

# test build
RUN cd llama.cpp && ./main -m ./models/orca_mini_v2_13b.ggmlv3.q2_K.bin -p "explain the negative energy spike when teleporting a qubit according to ER=EPR" -n 512

#copy run file
COPY run-tensor /root/run-tensor
RUN chmod 744 /root/run*

ENV NVIDIA_VISIBLE_DEVICES all
ENV NVIDIA_DRIVER_CAPABILITIES graphics,utility,compute
ENTRYPOINT /root/run
