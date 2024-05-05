FROM twobombs/qrackmin

# fetch dependancies
RUN export DEBIAN_FRONTEND=noninteractive && apt update && apt install -y git python3-pip mc sudo wget libopenblas-dev libclblast-dev mysql-server && apt clean all

# fetch llama-cpp-python
RUN git clone --depth=1 --recursive -j8 https://github.com/abetlen/llama-cpp-python.git

# fetch ollama
RUN curl -fsSL https://ollama.com/install.sh | sh

# fetch and unpack qrack QFT/QNN patterns
RUN git clone https://github.com/twobombs/thereminq-bonsai.git
RUN cd thereminq-bonsai/miscfiles && for file in *.tar.gz; do tar -xzf "$file"; done

# fetch autogenstudio, crewai
# RUN pip3 install autogenstudio crewai[tools] open-interpreter && pip cache purge

#load default model
RUN wget https://huggingface.co/mradermacher/Llama-3-DARE-8B-GGUF/resolve/main/Llama-3-DARE-8B.IQ3_M.gguf

#copy run file
COPY /runfiles/run-* /root
RUN chmod 744 /root/run*

ENV NVIDIA_VISIBLE_DEVICES all
ENV NVIDIA_DRIVER_CAPABILITIES graphics,utility,compute
ENV HOST 0.0.0.0

EXPOSE 80 5173 7680 7861 8000 8081 8501 8080 11434
ENTRYPOINT /root/run-llama
