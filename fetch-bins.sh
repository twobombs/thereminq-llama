#!/bin/bash
# fetch bins from huggingface
# 450 GB - might take a while

# sources
# https://huggingface.co/decapoda-research
# https://huggingface.co/Sosaka
# https://huggingface.co/TheBloke
# https://huggingface.co/Pi3141

apt install -y git git-lfs

git clone https://huggingface.co/decapoda-research/llama-65b-hf &
git clone https://huggingface.co/decapoda-research/llama-7b-hf &
git clone https://huggingface.co/decapoda-research/llama-30b-hf &

git clone https://huggingface.co/openlm-research/open_llama_7b_preview_200bt &
git clone https://huggingface.co/openlm-research/open_llama_7b_preview_300bt &

git clone https://huggingface.co/TheBloke/alpaca-lora-65B-GGML &
git clone https://huggingface.co/Sosaka/Alpaca-native-4bit-ggml &

# test for new ggml @llama.cpp
wget https://huggingface.co/Pi3141/alpaca-native-13B-ggml/resolve/main/ggml-model-q8_0.bin

# https://www.together.xyz/blog/redpajama
# this one will take 3TB > 8TB extracted
mkdir Redpajama-LLaMa-1T && cd Redpajama-LLaMa-1T
wget 'https://data.together.xyz/redpajama-data-1T/v1.0.0/urls.txt'
while read line; do
    dload_loc=${line#https://data.together.xyz/redpajama-data-1T/v1.0.0/}
    mkdir -p $(dirname $dload_loc)
    wget "$line" -O "$dload_loc"
done < urls.txt
