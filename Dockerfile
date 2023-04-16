FROM twobombs/qrackmin:pocl

RUN curl -o ./models/ggml-alpaca-7b-q4.bin -C - https://ipfs.io/ipfs/QmUp1UGeQFDqJKvtjbSYPBiZZKRjLp8shVP9hT8ZB9Ynv1
RUN git clone https://github.com/ggerganov/llama.cpp && cd llama.cpp && make -j && ./main -m ./models/7B/ggml-model-q4_0.bin -p "explain the negative energy spike when teleporting a qubit according to ER=EPR" -n 512

ENV NVIDIA_VISIBLE_DEVICES all
ENV NVIDIA_DRIVER_CAPABILITIES graphics,utility,compute
ENTRYPOINT /root/run
