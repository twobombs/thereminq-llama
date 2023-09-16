FROM twobombs/qrackmin

# fetch dependancies
RUN export DEBIAN_FRONTEND=noninteractive && apt update && apt install -y git python3-pip mc wget libopenblas-dev libclblast-dev && apt clean all

# fetch llama-cpp-python
RUN git clone --recursive -j8 https://github.com/abetlen/llama-cpp-python.git

#load default model
RUN wget https://huggingface.co/TheBloke/WizardMath-7B-V1.0-GGUF/resolve/main/wizardmath-7b-v1.0.Q2_K.gguf

#copy run file
COPY /runfiles/run-* /root
RUN chmod 744 /root/run*

ENV NVIDIA_VISIBLE_DEVICES all
ENV NVIDIA_DRIVER_CAPABILITIES graphics,utility,compute

EXPOSE 80 5173 7680
ENTRYPOINT /root/run-llama
