FROM twobombs/qrackmin:2204

# fetch dependancies
RUN export DEBIAN_FRONTEND=noninteractive && apt update && apt install -y git python3-pip mc sudo wget libopenblas-dev libclblast-dev && apt clean all

# fetch llama-cpp-python
RUN git clone --depth=1 --recursive -j8 https://github.com/abetlen/llama-cpp-python.git

#load default model
RUN wget https://huggingface.co/TheBloke/WizardMath-7B-V1.1-GGUF/resolve/main/wizardmath-7b-v1.1.Q2_K.gguf

# fetch Qrack/Sycamore measured results and SDRP/fidelity scores
RUN git clone --depth=1 https://github.com/twobombs/thereminq
RUN git clone --depth=1 https://github.com/twobombs/thereminq-bonsai

#copy run file
COPY /runfiles/run-* /root
RUN chmod 744 /root/run*

ENV NVIDIA_VISIBLE_DEVICES all
ENV NVIDIA_DRIVER_CAPABILITIES graphics,utility,compute

EXPOSE 80 5173 5601 7680 9200
ENTRYPOINT /root/run-llama
