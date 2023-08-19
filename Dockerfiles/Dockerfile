FROM twobombs/qrackmin

# fetch dependancies
RUN export DEBIAN_FRONTEND=noninteractive && apt update && apt install -y git python3-pip mc wget libopenblas-dev libclblast-dev && apt clean all

# fetch llama-cpp-python
RUN git clone --recursive -j8 https://github.com/abetlen/llama-cpp-python.git

#load default model
RUN wget https://huggingface.co/TheBloke/orca_mini_v2_13b-GGML/resolve/main/orca_mini_v2_13b.ggmlv3.q2_K.bin

#copy run file
COPY /runfiles/run-* /root
RUN chmod 744 /root/run*

ENV NVIDIA_VISIBLE_DEVICES all
ENV NVIDIA_DRIVER_CAPABILITIES graphics,utility,compute
ENTRYPOINT /root/run
