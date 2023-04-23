# thereminq-llama : baking a quantum layer caek
This repo is alpha and dedicated to training LLama's with QC data

Download bin files through fetch-bins.sh and start container with nvdia-docker support
--------

start the container image with default settings it has ggml-alpaca-7b-q4 included in the image with llama.cpp as the driver

docker run -v /[dowloadpath][model]/:/llama.cpp/models -it --rm twobombs/thereminq-llama

--------
![Untitled](https://user-images.githubusercontent.com/12692227/232248160-f4c2a3aa-fd19-4b62-b6f2-532ec44ca0e3.png)
