FROM twobombs/cudacluster:2204dev
# FROM twobombs/qrackmin
# FROM nvidia/cuda:12.2.2-devel-ubuntu22.04
LABEL com.nvidia.volumes.needed="nvidia_driver"

ENV PATH /usr/local/nvidia/bin:${PATH}
ENV LD_LIBRARY_PATH /usr/local/nvidia/lib:/usr/local/nvidia/lib64:${LD_LIBRARY_PATH}

# fetch qrack-dev deb package
RUN apt update && apt install -y software-properties-common && apt clean
RUN add-apt-repository -y ppa:wrathfulspatula/vm6502q && apt clean
RUN apt install -y libqrack-dev

# HF and Open-interpreter dependancies
RUN export DEBIAN_FRONTEND=noninteractive && apt install -y python3-pip npm ipython3 python-is-python3 ffmpeg python3-venv git-lfs libgl1 libglib2.0-0 && apt clean all
RUN apt remove python3-kiwisolver && pip3 install huggingface_hub[hf_transfer] open-interpreter && pip cache purge

# fetch llama-cpp-python
RUN git clone --depth=1 --recursive -j8 https://github.com/abetlen/llama-cpp-python.git

# fetch and unpack qrack QFT/QNN patterns
RUN git clone --depth=1 https://github.com/twobombs/thereminq-bonsai.git
RUN cd thereminq-bonsai/miscfiles && for file in *.tar.gz; do tar -xzf "$file"; done

# fetch ollama
RUN curl -fsSL https://ollama.com/install.sh | sh

# fetch gptscript, clio
# RUN apt install -y golang && apt clean all
# RUN curl https://get.gptscript.ai/install.sh | sh
# RUN git clone https://github.com/gptscript-ai/clio.git && cd clio && make build

# fetch autogenstudio, crewai
# RUN pip3 install autogenstudio crewai[tools] open-interpreter && pip cache purge

#load default model
RUN touch Meta-Llama-3.1-8B-q4_k_s.gguf

#copy run file
COPY /runfiles/run-* /root
RUN chmod 744 /root/run*

ENV NVIDIA_VISIBLE_DEVICES all
ENV NVIDIA_DRIVER_CAPABILITIES graphics,utility,compute
ENV HOST 0.0.0.0

EXPOSE 80 3000 5173 7680 7861 8000 8081 8501 8080 11434
ENTRYPOINT /root/run-llama
