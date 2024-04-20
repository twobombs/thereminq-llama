FROM twobombs/qrackmin

# fetch dependancies
RUN export DEBIAN_FRONTEND=noninteractive && apt update && apt install -y git python3-pip mc sudo wget libopenblas-dev libclblast-dev mysql-server && apt clean all

# fetch llama-cpp-python
RUN git clone --depth=1 --recursive -j8 https://github.com/abetlen/llama-cpp-python.git

# langchain and mlflow
RUN python3 -m pip install --upgrade langchain mlflow

# fetch autogenstudio, crewai
RUN pip3 install autogenstudio crewai[tools]

#load default model
RUN wget https://huggingface.co/TheBloke/WizardMath-7B-V1.1-GGUF/resolve/main/wizardmath-7b-v1.1.Q2_K.gguf

# fetch Qrack/Sycamore measured results and SDRP/fidelity scores
# RUN git clone --depth=1 https://github.com/twobombs/thereminq
RUN git clone --depth=1 https://github.com/twobombs/thereminq-bonsai

#copy run file
COPY /runfiles/run-* /root
RUN chmod 744 /root/run*

ENV NVIDIA_VISIBLE_DEVICES all
ENV NVIDIA_DRIVER_CAPABILITIES graphics,utility,compute
ENV HOST 0.0.0.0

EXPOSE 80 5173 7680 7861 8081
ENTRYPOINT /root/run-llama
