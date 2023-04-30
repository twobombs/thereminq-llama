FROM twobombs/qrackmin:pocl

# fetch nod-ai, lit-llama & llama.cpp
RUN git clone https://github.com/ggerganov/llama.cpp 
RUN git clone https://github.com/nod-ai/llama.git
RUN git clone https://github.com/Lightning-AI/lit-llama

ENV NVIDIA_VISIBLE_DEVICES all
ENV NVIDIA_DRIVER_CAPABILITIES graphics,utility,compute
ENTRYPOINT /root/run
