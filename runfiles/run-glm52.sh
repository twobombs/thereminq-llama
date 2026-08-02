numactl --cpunodebind=4-7 --membind=4-7 \
  ./llama-vulkan/build/bin/llama-server \
  -m /media/aryan/nvme/models/GLM-52/UD-IQ1S/GLM-5.2-UD-IQ1_S-00001-of-00006.gguf \
  --tools all \
  -c 32768 \
  -np 1 \
  -ngl 0 \
  --load-mode mmap \
  -fa on \
  -t 48 -tb 48 \
  --reasoning on \
  --reasoning-preserve \
  --host 0.0.0.0 \
  --port 8033 \
  --cors-origins "*" \
  -ctk q8_0 -ctv q8_0
