#!/bin/bash
# fetch bins from huggingface
# 450 GB - might take a while

# sources
# https://huggingface.co/decapoda-research
# https://huggingface.co/Sosaka
# https://huggingface.co/TheBloke
# https://huggingface.co/Pi3141

apt install -y git git-lfs

# a zoo of old(er) LLaMa's
git clone https://huggingface.co/decapoda-research/llama-65b-hf &
git clone https://huggingface.co/decapoda-research/llama-7b-hf &
git clone https://huggingface.co/decapoda-research/llama-30b-hf &

git clone https://huggingface.co/openlm-research/open_llama_7b_preview_200bt &
git clone https://huggingface.co/openlm-research/open_llama_7b_preview_300bt &

git clone https://huggingface.co/TheBloke/alpaca-lora-65B-GGML &
git clone https://huggingface.co/Sosaka/Alpaca-native-4bit-ggml &

# test for newer ggml @llama.cpp
wget https://huggingface.co/Pi3141/alpaca-native-13B-ggml/resolve/main/ggml-model-q8_0.bin &

# quantized wizard llm 
wget https://huggingface.co/TheBloke/WizardLM-13B-V1.2-GGML/resolve/main/wizardlm-13b-v1.2.ggmlv3.q2_K.bin

