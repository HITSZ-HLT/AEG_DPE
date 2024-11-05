CUDA_VISIBLE_DEVICES=3 /home/heyuhang/miniconda3/envs/llm/bin/python example_writing.py \
    --backend llama7b-hf \
    --dataset_name en_ArgEssay \
    --prompt_column prompt \
    --response_column essay \
    --method gotDPE \


CUDA_VISIBLE_DEVICES=3 /home/heyuhang/miniconda3/envs/llm/bin/python example_writing.py \
    --backend llama7b-hf \
    --dataset_name en_NYT \
    --prompt_column instruction \
    --response_column article_content \
    --method gotDPE \