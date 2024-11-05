CUDA_VISIBLE_DEVICES=3 /home/heyuhang/miniconda3/envs/llm/bin/python example_writing.py \
    --backend Baichuan2-7B \
    --dataset_name zh_ArgEssay \
    --prompt_column instruction \
    --response_column article_content \
    --method gotDPE \

CUDA_VISIBLE_DEVICES=0 /home/heyuhang/miniconda3/envs/llm/bin/python example_writing.py \
    --backend Baichuan2-7B \
    --dataset_name zh_News \
    --prompt_column instruction \
    --response_column article_content \
    --method gotDPE