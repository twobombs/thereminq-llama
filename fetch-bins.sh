#!/bin/bash
# fetch bins from huggingface
# 430+ GB - might take a while
# sources - https://huggingface.co/decapoda-research, https://huggingface.co/Sosaka & https://huggingface.co/TheBloke 

apt install -y git git-lfs

git clone https://huggingface.co/decapoda-research/llama-65b-hf &
git clone https://huggingface.co/decapoda-research/llama-7b-hf &
git clone https://huggingface.co/decapoda-research/llama-30b-hf &

git clone https://huggingface.co/openlm-research/open_llama_7b_preview_200bt &
git clone https://huggingface.co/openlm-research/open_llama_7b_preview_300bt &

git clone https://huggingface.co/TheBloke/alpaca-lora-65B-GGML &
git clone https://huggingface.co/Sosaka/Alpaca-native-4bit-ggml &
