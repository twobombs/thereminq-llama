FROM twobombs/qrackmin:pocl

RUN git clone https://github.com/ggerganov/llama.cpp 
RUN cd llama.cpp/models && wget https://huggingface.co/Sosaka/Alpaca-native-4bit-ggml/resolve/main/ggml-alpaca-7b-q4.bin 
RUN cd llama.cpp && make -j && ./main -m ./models/ggml-alpaca-7b-q4.bin -p "explain the negative energy spike when teleporting a qubit according to ER=EPR" -n 512

ENV NVIDIA_VISIBLE_DEVICES all
ENV NVIDIA_DRIVER_CAPABILITIES graphics,utility,compute
ENTRYPOINT /root/run
