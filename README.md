# ThereminQ-LLaMa : baking a quantum layer caek

This repo is alpha and dedicated to training Lggml Lama's with QC data

- ggml-model-q8_0.bin included in the image, otherwise mount the model with -v
 
--------

CPU - llama.cpp OpenBLAS

docker run -it --rm twobombs/thereminq-llama:cpu

--------

GPU - llama.cpp OpenBLAS & cuBLAS

docker run --gpus all -it --rm twobombs/thereminq-llama:gpu

--------
- Download bin files through fetch-bins.sh and start container with nvdia-docker support

--------
![Untitled](https://user-images.githubusercontent.com/12692227/232248160-f4c2a3aa-fd19-4b62-b6f2-532ec44ca0e3.png)
