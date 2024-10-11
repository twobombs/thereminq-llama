# ThereminQ-llama : baking a Quantum layer caek

This repo is alpha and dedicated to extending `GGUF` llama LLMs with QC data on Agent steriods
- new features will pop up in other ThereminQ repos
- this repo currently serves to test functionality 

Functionality added to the ThereminQ stack so far
- agency to ThereminQ-tensors

![2a40063099465fee941a701289810666](https://github.com/twobombs/thereminq-llama/assets/12692227/6097d5e2-92fa-4bff-9297-c26d98f31d84)

--------

`Qrackmin` + `llama.cpp` + `open-interpreter` + `` integrated container image stack

```bash
docker run --gpus all -v /path-to-/models:/text-generation-webui/models  -p 5000:5000 -p 5173:5173 -p 5601:5601 -p 6080:6080 -p 7860:7860 -p 8501:8501 -p 8081:8081 -d twobombs/thereminq-llama[:tag] 
````

- `latest` includes QC/AI dependancies and downloads a LLama3 model
- `cli` LLama.cpp compiled versions for direct CLI interaction such as model [conversion](https://github.com/ggerganov/llama.cpp?tab=readme-ov-file#prepare-and-quantize)
- `chatui` for web based LLM interfaces & huggingface URL tunnel
- `agent` for OpenInterpreterUI/CLI with Ollama3 integration
- `big-agency` Autogen Studio integrated with Ollama UI

--------

![Screenshot from 2024-06-01 10-15-20](https://github.com/twobombs/thereminq-llama/assets/12692227/4c5ddfea-74fc-4251-ae21-776642f2de0f)

![Screenshot from 2024-06-01 10-20-29](https://github.com/twobombs/thereminq-llama/assets/12692227/cdf5e11d-c7a1-484b-926c-b25bb262ecb6)

![Screenshot from 2024-06-01 10-24-37](https://github.com/twobombs/thereminq-llama/assets/12692227/5c0b52a0-92bd-4f5e-8ff0-5fb008ad15db)


--------

Work in progress 

![QCAI-chat drawio](https://github.com/twobombs/thereminq-llama/assets/12692227/53d15ddb-1599-4787-bc0e-962672d81cf1)


--------

Optional
- Download a ton of hugging face bin files through [fetch-bins.sh](https://github.com/twobombs/thereminq-llama/blob/main/misc/fetch-bins.sh)

--------

Credits for Qrack, LLaMa.cpp and Open Interpreter go to

Dan Strano https://github.com/unitaryfund/qrack

Georgi Gerganov https://github.com/ggerganov/llama.cpp

Open Interpreter project https://www.openinterpreter.com/

AutoGen Studio https://autogen-studio.com/

... and their respective contributers

--------

![Untitled](https://user-images.githubusercontent.com/12692227/232248160-f4c2a3aa-fd19-4b62-b6f2-532ec44ca0e3.png)

poem generated by [ChatGPT 3](https://chat.openai.com/)
