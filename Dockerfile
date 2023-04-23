FROM twobombs/qrackmin:pocl

RUN cd models && wget https://ipfs.io/ipfs/QmUp1UGeQFDqJKvtjbSYPBiZZKRjLp8shVP9hT8ZB9Ynv1
RUN git clone https://github.com/ggerganov/llama.cpp 
RUN cd llama.cpp/models && wget -O ggml-alpaca-7b-q4.bin https://ipfs.io/ipfs/QmUp1UGeQFDqJKvtjbSYPBiZZKRjLp8shVP9hT8ZB9Ynv1 
RUN cd llama.cpp && make -j && ./main -m ./models/ggml-alpaca-7b-q4.bin -p "explain the negative energy spike when teleporting a qubit according to ER=EPR" -n 512

ENV NVIDIA_VISIBLE_DEVICES all
ENV NVIDIA_DRIVER_CAPABILITIES graphics,utility,compute
ENTRYPOINT /root/run
