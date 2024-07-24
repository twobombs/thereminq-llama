#!/bin/bash
cd /llama-cublas
python convert_hf_to_gguf.py <pathtomodel> --outtype f32
./bin/llama-quantize <pathtomodel>/ggml-model-f32.gguf Q4_K_S
