#!/bin/bash
# fetch bins from huggingface
# 1.4+ TB - might take a while
# sources - 
# https://huggingface.co/decapoda-research
# https://huggingface.co/Sosaka
# https://www.together.xyz/blog/redpajama
# https://huggingface.co/TheBloke 

apt install -y git git-lfs

git clone https://huggingface.co/decapoda-research/llama-65b-hf &
git clone https://huggingface.co/decapoda-research/llama-7b-hf &
git clone https://huggingface.co/decapoda-research/llama-30b-hf &

git clone https://huggingface.co/openlm-research/open_llama_7b_preview_200bt &
git clone https://huggingface.co/openlm-research/open_llama_7b_preview_300bt &

git clone https://huggingface.co/TheBloke/alpaca-lora-65B-GGML &
git clone https://huggingface.co/Sosaka/Alpaca-native-4bit-ggml &

mkdir Redpajama-LLaMa-1T && cd Redpajama-LLaMa-1T
wget 'https://data.together.xyz/redpajama-data-1T/v1.0.0/urls.txt'
while read line; do
    dload_loc=${line#https://data.together.xyz/redpajama-data-1T/v1.0.0/}
    mkdir -p $(dirname $dload_loc)
    wget "$line" -O "$dload_loc"
done < urls.txt
