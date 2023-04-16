# thereminq-llama : baking a quantum layer caek
This repo is alpha and dedicated to training LLama's with QC data

Download bin files through fetch-bins.sh and start container with nvdia-docker support

docker run --gpus all --ipc=host --ulimit memlock=-1 -v /[dowloadpath]llama-7b-hf/:/app/models -p 7860:7860 -it --rm twobombs/llama-docker-playground:llama

Container image is derivate of [https://github.com/soulteary/llama-docker-playground](https://github.com/soulteary/llama-docker-playground/blob/main/docker/Dockerfile.llama)
--------
![Untitled](https://user-images.githubusercontent.com/12692227/232248160-f4c2a3aa-fd19-4b62-b6f2-532ec44ca0e3.png)
