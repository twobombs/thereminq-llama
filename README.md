# ThereminQ-LLaMa : baking a quantum layer caek

This repo is alpha and dedicated to training ggml LLaMa's with QC data

![2a40063099465fee941a701289810666](https://github.com/twobombs/thereminq-llama/assets/12692227/6097d5e2-92fa-4bff-9297-c26d98f31d84)

--------

Qrackmin:POCL + LLaMa.cpp integrated container image

docker run --privileged --gpus all -d twobombs/thereminq-llama[:tag]
- latest for model and cpu
- cl for additional llama.cpp opencl support
- cuda for additional llama.cpp cuda support
- spark for llama-cpp-python and spark services

--------

Optional
- Download a ton of hugging face bin files through fetch-bins.sh and start container with or without nvdia-docker support

--------

Credits for Qrack and LLaMa.cpp go to

Dan Strano https://github.com/unitaryfund/qrack

Georgi Gerganov https://github.com/ggerganov/llama.cpp

... and their respective contributers

--------
![Untitled](https://user-images.githubusercontent.com/12692227/232248160-f4c2a3aa-fd19-4b62-b6f2-532ec44ca0e3.png)

poem generated by ChatGPT 3
