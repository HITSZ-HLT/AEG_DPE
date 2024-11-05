/home/heyuhang/miniconda3/envs/llm/bin/python example_writing.py \
    --backend llama7b-hf \
    --dataset_name en_ArgEssay \
    --prompt_column instruction \
    --response_column article_content \
    --method got \


/home/heyuhang/miniconda3/envs/llm/bin/python example_writing.py \
    --backend chatgpt \
    --dataset_name en_NYT \
    --prompt_column instruction \
    --response_column article_content \
    --method got \

/home/heyuhang/miniconda3/envs/llm/bin/python example_writing.py \
    --backend chatgpt \
    --dataset_name zh_ArgEssay \
    --prompt_column instruction \
    --response_column article_content \
    --method cot

/home/heyuhang/miniconda3/envs/llm/bin/python example_writing.py \
    --backend chatgpt \
    --dataset_name zh_News \
    --prompt_column instruction \
    --response_column article_content \
    --method io \
    --resume_path results/zh_News/chatgpt_io_2023-11-30_03-26-58 \


